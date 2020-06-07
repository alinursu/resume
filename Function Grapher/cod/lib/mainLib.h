/**********************************************************************************
---------------------- Libraria principala-----------------------------------------
Aici se includ celelalte librarii, plus cateva functii ajutatoare
***********************************************************************************/
// Constante folosite
const double PI = 3.141592653589793115997963468544185161590576171875; // Pi constant
const double E = 2.718281828459045090795598298427648842334747314453125; // Euler constant
const double EPSILON = 0.000001; // Epsilon - reprezentare numar foarte mic (>0)
const double INFINIT = 99999999999999.0;// Infinit - reprezentare numar foarte mare

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "stack.h"
#include "binaryTree.h"
#include "mathFunctions.h"
#include "variable.h"
#include "converters.h"
using namespace std;

struct Errors {
    char* errorMessage;
    Errors* next;
};

struct Errors *error[120]; // Un vector care va memora erorile

Errors* newError(char* errorMessage) {
	// Functie pentru construirea unei erori
    Errors* newErr = (Errors*)malloc(sizeof(Errors));
    newErr->errorMessage = errorMessage;
    newErr->next = NULL;
    return newErr;
}

void addError(char* errorText, int position) {
	// Functie de adaugare a unei erori
    char* tempErr = (char*)malloc((100)*sizeof(char));
    sprintf(tempErr, "Pozitia %d->%s", position, errorText);
    if (error[position] == NULL) {
        error[position] = newError(tempErr);
        return;
    }
    Errors* newErr = newError(tempErr);
    newErr->next = error[position];
    error[position] = newErr;
}

void deleteErrors() {
	// Stergerea/Resetarea erorilor
    for (int i = 0; i < 120; i++) {
        if (error[i] != NULL) {
            while (error[i] != NULL) {
                Errors* tempErr = error[i];
                error[i] = error[i]->next;
                free(tempErr->errorMessage);
                free(tempErr);
                tempErr = NULL;
            }
        }
    }
}

int numberOfDecimalPoints(char word[]) {
	// Calculeaza numarul de puncte decimale/virgule dintr-un cuvant
    int length = strlen(word);
    int nrPoints = 0;
    for (int i = 0; i < length; ++i)
        if (word[i] == '.')
            nrPoints++;

    return nrPoints;
}

bool isDigitOrLetter(char ch) {
	// Verifica daca caracterul dat este o cifra sau o litera, se accepta si virgula/punctul
    if ((ch >= '0' && ch <= '9')||(ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || (ch=='.') || (ch == ','))
        return true;
    return false;
}

char* strToLower(char*);
bool isUnaryOperator(char* opr) {
	// Verifica daca este operator unar
    switch(opr[0]) {
        case 'a':
            if (!strcmp(opr, "abs") || !strcmp(opr, "asin") || !strcmp(opr, "acos") || !strcmp(opr, "atan") || !strcmp(opr, "actg"))
                return true;
            else
                return false;
        case 'c':
            if (!strcmp(opr, "ctg") || !strcmp(opr, "cos"))
                return true;
            else
                return false;
        case 'l':
            if (!strncmp(opr, "ln", 2) || !strncmp(opr, "log2", 4) || !strncmp(opr, "log", 3))
                return true;
            else
                return false;
        case 's':
            if (!strcmp(opr, "sin") || !strcmp(opr, "sqrt"))
                return true;
            else
                return false;
        case 't':
            if (!strcmp(opr, "tan"))
                return true;
            else
                return false;
        case '-':
            if (!strcmp(opr, "-u")) // minus unar
                return true;
            else
                return false;
        case '+':
            if (!strcmp(opr, "+u")) // plus unar
                return true;
            else
                return false;
        default:
            return false;
    }
}

bool isBinaryOperator(char* opr) {
	// Verfica daca este operator binar
    switch(opr[0]) {
        case '+':
        case '-':
            if (isUnaryOperator(opr))
                return false;
            else
                return true;
            break;
        case '*':
        case '/':
        case '%':
        case '^':
        case '#':
            return true;
        case '<':
            if (!strcmp(opr, "<") || !strcmp(opr, "<=") || !strcmp(opr, "<>"))
                return true;
            else
                return false;
        case '>':
            if (!strcmp(opr, ">") || !strcmp(opr, ">="))
                return true;
            else
                return false;
        case '=':
            return true;
        default:
            return false;
    }
}

bool isOperand(char* operand) {
	// Verifica daca este operand valid sau nu
    if (isUnaryOperator(operand) || isBinaryOperator(operand))
        return false;

    bool isVariable;
    int length = strlen(operand);


    if (operand[0] == '(' || operand[0] == ')')
        return false;

    if ((operand[0] >= '0' && operand[0] <= '9') || operand[0] == '.')
        isVariable = false; // Ar trebui sa fie un numar
    else
        isVariable = true; // Ar trebui sa fie o variabila


    for (int i=1; i < length; i++) {
        if (isVariable && operand[i] == '.')
            return false;
        else if (!isVariable)
            if ((operand[i] >= 'A' && operand[i] <= 'Z') || (operand[i] >= 'a' && operand[i] <= 'z'))
                return false;
        if (!isDigitOrLetter(operand[i]))
            return false;
    }
    return true;
}

int operatorPriority(char* opr) {
	// Verifica prioritatea operatorilor
    switch(opr[0]) {
        case '-':
            if (!strcmp(opr, "-u"))
                return 5;
            else
                return 1;
            break;
        case '+':
            if (!strcmp(opr, "+u"))
                return 5;
            else
                return 1;
            break;
        case '*':
        case '/':
        case '%':
            return 2;
        case '^':
            return 3;
        case '=':
        case '>':       //>, >=
        case '<':       //<, <=, <>
        case '#':
            return 4;
        case 'a':       //abs
        case 'c':       //ctg
        case 'l':       //ln, log, log2
        case 's':       //sin, sqrt
        case 't':       //tan
            return 6;
        default:
            return -1;
    }
}

// Structura pentru a memora date despre expresie
struct Expression {
    char *expression; // Expresia implicita
    char infixVec[105][30]; // Vectorul de cuvinte
    char postfixVec[105][30]; // Vectorul de cuvinte in ordine postfixata
    int infixLength; // Lungimea vecorului de cuvinte in ordine infixata
    bool isOK; // Este sau nu corecta din punct de vdere sintactic
}Functie;


char* removeSpaces(char* exp);
void createVector(struct Expression&);
void setExpression(struct Expression &newE, char* expression) {
    newE.isOK = true;
    newE.infixLength = 0;
    if (expression == NULL)
        return;
    else {
        newE.expression = expression;
        removeSpaces(newE.expression);
        createVector(newE);
    }
}

char* removeSpaces(char* str) {
	// Functie pentru stergerea spatiilor din expresie
    int i = 0, j = 0;
    while (str[i]) {
        if (str[i] != ' ')
            str[j++] = str[i];
        i++;
    }
    str[j] = '\0';
    return str;
}

char* addSpacesIn(struct Expression& input) {
	// Functie ce va adauga spatii intre cuvinte
    int newIndex = -1;
    int i = 0;

    char* expr = (char*)malloc(105*sizeof(char));
    strcpy(expr, input.expression);

    int len = strlen(expr);

    char* temp = (char*)malloc(200*sizeof(char));
    *temp = 0;

    while (i < len) {
        char tempc[2] = "";
        sprintf(tempc, "%c",expr[i]);
        if (isDigitOrLetter(expr[i]) || expr[i] == '.' || expr[i] == ',') {
            temp[++newIndex] = expr[i];
            i++;
        } else if (isBinaryOperator(tempc)) {
            if ((i > 0 && expr[i-1] != '<' && expr[i-1] != '>') || (expr[i] != '=' && expr[i] != '>'))
                temp[++newIndex] = ' ';

            temp[++newIndex] = expr[i];

            // Daca este minus sau plus ca operator unar
            if ((i == 0 || expr[i-1] == '(')  && (expr[i] == '-' || expr[i] == '+') )
                temp[++newIndex] = 'u';
            if(i < len-1 && isDigitOrLetter(expr[i+1]))
                temp[++newIndex] = ' ';
            i++;
        } else if (expr[i] == '(' || expr[i] == ')') {
            temp[++newIndex] = ' ';
            temp[++newIndex] = expr[i];
            temp[++newIndex] = ' ';
            i++;
        } else {
            temp[++newIndex] = expr[i];
            temp[++newIndex] = ' ';
            i++;
        }
    }
    temp[++newIndex] = '\0';
    free(expr);
    return temp;
}

void createVector(struct Expression& input) {
	// Functie ce va crea vectorul de cuvinte
    char* word;
    char* tempWords = addSpacesIn(input);
    int length = 0;

    word = strtok(tempWords, " ");
    while (word != NULL) {
        strcpy(input.infixVec[length++], word);
        word = strtok(NULL, " ");
    }

    input.infixVec[length][0] = 0;
    input.infixLength = length;

    free(tempWords);
}

bool isValidExpression(Expression& input) {
	// Functie ce verfica daca expresia este sau nu este corecta din punct de vedere sintactic
    if (input.expression == NULL)
        return true;
    input.isOK = true;
    char error[120] = "";
    char aux[50] = "";
    char* tempW;
    int paranthesis = 0;
    int i;
    int position = 0;

    deleteErrors();

    for(i=0; i<input.infixLength; ++i) {
        position = position + strlen(input.infixVec[i]);

        strcpy(aux, input.infixVec[i]);
        tempW = (char*)strtok(aux, ".");
        if (strlen(tempW) > 12) {
            strcpy(error, "Eroare: Numerele/Variabile pot avea maxim 12 cifre/caractere!");
            addError(error,position-strlen(input.infixVec[i])+1);
            input.isOK = false;
        } // Lungimea maxima a unei variabile/numar este de 12 cifre/caractere

        if (!isOperand(input.infixVec[i]) && !isBinaryOperator(input.infixVec[i])&& !isUnaryOperator(input.infixVec[i])) {
            if (strcmp(input.infixVec[i], ")") && strcmp(input.infixVec[i], "(")) {
                strcpy(error, "Eroare: Numele variabilei nu este valid!");
                addError(error,position-strlen(input.infixVec[i])+1);
                input.isOK = false;
            }
        } // Cuvantul nu este valid
        if (isOperand(input.infixVec[i]) && numberOfDecimalPoints(input.infixVec[i]) > 1) {
            strcpy(error, "Eroare: Numarul are prea multe virgule!");
            addError(error,position-strlen(input.infixVec[i])+1);
            input.isOK = false;
        } // Daca numarul are mai mult de o virgula
        if(input.infixVec[i][0]=='(') {
            if (i == input.infixLength-1) {
                strcpy (error, "Eroare: Dupa \"(\" expresia se termina brusc!");
                addError(error,position);
                input.isOK = false;
            }
            if (i > 0 && isOperand(input.infixVec[i-1])) {
                strcpy (error, "Eroare: Inainte de \"(\" este un numar/variabila");
                addError(error,position);
                input.isOK = false;
            }
            if (i < input.infixLength - 1 && isBinaryOperator(input.infixVec[i+1])) {
                strcpy (error, "Eroare: Dupa \"(\" este un operator binar");
                addError(error,position);
                input.isOK = false;
            }
            paranthesis++;
        } // Erori cu paranteza deschisa
        if(input.infixVec[i][0]==')') {
            if (i == 1) {
                strcpy(error, "Eroare: Paranteza inchisa la inceputul expresiei!");
                addError(error,position);
                input.isOK = false;
            }
            if (i < input.infixLength - 1 && !strcmp(input.infixVec[i+1], "(")) {
                strcpy (error, "Eroare: Intre \")\" si \"(\" nu este nici un operator de tip binar");
                addError(error,position);
                input.isOK = false;
            }
            if (i < input.infixLength - 1 && isOperand(input.infixVec[i+1])) {
                strcpy (error, "Eroare: Dupa \")\" este un numar/variabila!");
                addError(error,position);
                input.isOK = false;
            }
            if (i > 0 && (isBinaryOperator(input.infixVec[i-1]) || isUnaryOperator(input.infixVec[i-1]))) {
                strcpy (error, "Eroare: Inainte de \")\" este un operator de tip binar/unar");
                addError(error,position);
                input.isOK = false;
            }
            if (i < input.infixLength - 1 && isUnaryOperator(input.infixVec[i+1])) {
                strcpy (error, "Eroare: Dupa \")\" este un operator de tip unar");
                addError(error,position);
                input.isOK = false;
            }
            paranthesis--;
            if (paranthesis < 0) {
                paranthesis++;
                strcpy (error, "Eroare: Avem o paranteza inchisa care nu se deschide");
                addError(error,position);
                input.isOK = false;
            }
        } // Erori cu paranteza inchisa

        if (i == input.infixLength-1 && isBinaryOperator(input.infixVec[i])) {
            strcpy(error, "Eroare: Expresia se termina cu un operator!");
            addError(error,position);
            input.isOK = false;
        } else if (i == input.infixLength-1 && isUnaryOperator(input.infixVec[i])) {
            strcpy (error, "Eroare: Expresia se termina cu un operator!");
            addError(error,position-strlen(input.infixVec[i])+1);
            input.isOK = false;
        }

        if(i < input.infixLength - 1) {
            if(input.infixVec[i][0]=='(' && input.infixVec[i+1][0]==')') {
                strcpy(error, "Eroare: Se asteapta o valoare sau o expresie intre paranteze!");
                addError(error,position);
                input.isOK = false;
            }
            if (isBinaryOperator(input.infixVec[i]) && isBinaryOperator(input.infixVec[i+1])) {
                strcpy(error, "Eroare: Nu pot exista doi operatori pe pozitii consecutive!");
                addError(error,position);
                input.isOK = false;
            }
            if(isUnaryOperator(input.infixVec[i]) && strcmp(input.infixVec[i+1], "(")) {
                if (strcmp(input.infixVec[i], "-u") && strcmp(input.infixVec[i], "+u")) {
                    strcpy(error, "Eroare: Functia ");
                    strcat(error, input.infixVec[i]);
                    strcat(error, " nu are niciun argument!");
                    addError(error,position-strlen(input.infixVec[i])+1);
                    input.isOK = false;
                }
            }
        }

        if(i < input.infixLength - 2)
            if(isUnaryOperator(input.infixVec[i]) && input.infixVec[i+1][0]=='(' && input.infixVec[i+2][0]==')') {
                if (strcmp(input.infixVec[i], "-u") && strcmp(input.infixVec[i], "+u")) {
                    strcpy(error, "Eroare: Functia ");
                    strcat(error, input.infixVec[i]);
                    strcat(error, " nu are niciun argument!");
                    addError(error,position-strlen(input.infixVec[i])+1);
                    input.isOK = false;
                }
            }
    }

    if(paranthesis != 0) {
        if (paranthesis > 0) {
            strcpy(error, "Eroare:Nu toate parantezele deschise se inchid!");
            addError(error, 0);
        } else {
            strcpy(error, "Eroare:Sunt mai multe paranteze inchise decat deschise!");
            addError(error, 0);
        }
        input.isOK = false;
    } // Erori parantezare

    return input.isOK;
} // Sfarsit isValidExpression


bool checkOperatorPrecedence(char*, Stack*);
void infixToPostfix(Expression& input) {
	// Transforma expresia din ordine infixata in ordine postfixata
    Stack* tempStack = NULL;
    int i = 0, k = -1;
    while (i < input.infixLength) {
        // Daca cuvantul scanat este un operand atunci il aduga direct in expresia postficata
        if (isOperand(input.infixVec[i]))
            strcpy(input.postfixVec[++k], input.infixVec[i]);
        // Daca cuvantul scanat este o paranteza deschisa o adauga in stiva
        else if (*input.infixVec[i] == '(')
            push(tempStack, input.infixVec[i]);
        // Daca cuvantul scanat este o paranteza inchisa,elimina si pune din stiva elementele in expresia postfixata
        // Pana la intalnirea unei paranteze deschise
        else if (*input.infixVec[i] == ')') {
            while (!isEmpty(tempStack) && *(char*)top(tempStack) != '(')
                strcpy(input.postfixVec[++k], (char*)pop(tempStack));
            pop(tempStack);
        }

        // Daca cuvantul scanat este un operator
        else {
            while (!isEmpty(tempStack) && checkOperatorPrecedence(input.infixVec[i], tempStack))
                strcpy(input.postfixVec[++k],(char*)pop(tempStack));
            push(tempStack, input.infixVec[i]);
        }

        i++;
    }
    // Elimina toti operatorii din stiva
    while (!isEmpty(tempStack))
        strcpy(input.postfixVec[++k], (char*)pop(tempStack));

    input.postfixVec[++k][0] = 0;

    return;
}

bool checkOperatorPrecedence(char* infixVec, Stack* tempStack) {
	// Asigura ordinea corecta a efectuarii operatiilor
    if(operatorPriority(infixVec) <= operatorPriority((char*)top(tempStack)) && *infixVec != '^')
        return true;

    else if (operatorPriority(infixVec) <= operatorPriority((char*)top(tempStack)) && *infixVec == '^' && isUnaryOperator((char*)top(tempStack)))
        return true;
    else
        return false;
}

double evaluateExpression(treeNode* expressionTree) {
	// Evalueaza expresia
    if (expressionTree == NULL)
        return 0;

    if (expressionTree->left && expressionTree->right) {
        double leftValue = evaluateExpression(expressionTree->left);
        double rightValue = evaluateExpression(expressionTree->right);

        char* Operator = expressionTree->info;
        switch(*Operator) {
            case '+':
                return Plus(leftValue, rightValue);
            case '-':
                return Minus(leftValue, rightValue);
            case '*':
                return Multiply(leftValue, rightValue);
            case '/':
                return Divide(leftValue, rightValue);
            case '%':
                return Modulo(leftValue, rightValue);
            case '^':
                return Power(leftValue, rightValue);
            case '=':
                return Equal(leftValue, rightValue);
            case '#':
                return notEqual(leftValue, rightValue);
            case '<':
                if (!strcmp(Operator, "<="))
                    return lessOrEqual(leftValue, rightValue);
                else if (!strcmp(Operator, "<>"))
                    return notEqual(leftValue, rightValue);
                else if (!strcmp(Operator, "<"))
                    return Less(leftValue, rightValue);
                break;
            case '>':
                if (!strcmp(Operator, ">="))
                    return greaterOrEqual(leftValue, rightValue);
                else if (!strcmp(Operator, ">"))
                    return Greater(leftValue, rightValue);
                break;
            default:
                return 0;

        }
    } else if(expressionTree->left == NULL && expressionTree->right == NULL) {
        double value;
        value = convertToNumber(expressionTree->info);
        if (isnan(value)) {
            char* variableName = expressionTree->info;
            value = getVariableValue(vars, variableName);
        }
        if (value > INFINIT)
            return INFINITY;
        return value;
    } else if (expressionTree->right) {
        double value = evaluateExpression(expressionTree->right);

        char* Operator = strToLower(expressionTree->info);
        switch(*Operator) {
            case 'a':
                if (!strcmp(Operator, "abs"))
                    return Absolute(value);
                else if (!strcmp(Operator, "asin"))
                    return arcSinus(value);
                else if (!strcmp(Operator, "acos"))
                    return arcCosinus(value);
                else if (!strcmp(Operator, "atan"))
                    return arcTangent(value);
                else if (!strcmp(Operator, "actg"))
                    return arcCotangent(value);
                break;
            case 'c':
                if (!strcmp(Operator, "ctg"))
                    return Cotangent(value);
                if (!strcmp(Operator, "cos"))
                    return Cosinus(value);
                break;
            case 'l':
                if (!strcmp(Operator, "ln"))
                    return Log(value);
                else if (!strcmp(Operator, "log2"))
                    return LogInBase(value, 2);
                else if (!strcmp(Operator, "log"))
                    return LogInBase(value, 10);
                break;
            case 's':
                if (!strcmp(Operator, "sin"))
                    return Sinus(value);
                else if (!strcmp(Operator, "sqrt"))
                    return Radical(value);
                break;
            case 't':
                if (!strcmp(Operator, "tan"))
                    return Tangent(value);
                break;
            case '-':
                if (!strcmp(Operator, "-u"))
                    return UnaryMinus(value);
                break;
            case '+':
                if (!strcmp(Operator, "+u"))
                    return UnaryPlus(value);
                break;
            default:
                return 0;
        }
    }
    return 0;
}







