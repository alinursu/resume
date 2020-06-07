#ifndef MATHCONDITIONS_H
#define MATHCONDITIONS_H

#include "dataConversions.h"
#include <cstring>
#include <cmath>
#include <math.h>

#define NUMBERPOINTS 750
using namespace std;

struct Point
{
    float x;
    float y;
};

void createExpression(char* f)
{
    /*
        Face expresia calculabila.
    */
    setExpression(Functie, f);
    infixToPostfix(Functie);
    arboreExpresie = getExpressionTree(Functie.postfixVec);
}

float calculateFunction(float x)
{
    resetVariables(vars);
    addVariable(vars, "x", x);
    return evaluateExpression(arboreExpresie);
}

bool verifyLogarithmCondition(float a, float b, char f[], float step, char *logarithmType)
{
    /*
        Verifica conditia de existenta a logaritmului: argumentul trebuie sa fie >0.
        Functia returneaza true daca nu exista logaritm in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care logartimul exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, logarithmType) == NULL)
        return true;

    // Preiau logaritmii
    char aux[101], copyF[101];
    strcpy(copyF, f);
    int i;
    while(strstr(copyF, logarithmType))
    {
        strcpy(aux, strstr(copyF, logarithmType));
        i=0;
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        // Calculez punctele in care logaritmul nu este definit
        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(isnan(calculateFunction(val)) || (calculateFunction(val) == 0) || (isinf(calculateFunction(val))))
            {
                return false;
            }
        }
        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifyFractionCondition(float a, float b, char f[], float step)
{
    /*
        Verifica conditia de existenta a fractiei: numitorul trebuie sa fie diferit de 0.
        Functia returneaza true daca nu exista fractie in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care fractia exista, dar conditia nu este valida, returneaza false.
    */
    if(strchr(f, '/') == NULL)
        return true;

    // Preiau numitorii
    char aux[101], copyF[101];
    int i;
    strcpy(copyF, f);
    while(strchr(copyF, '/'))
    {
        strcpy(aux, strchr(copyF, '/'));

        // Verific daca este expresie
        if(aux[1] != '(')
        {
            // Verific daca fractia este de forma 1/x
            if(aux[1] == 'x')
            {
                if((a <= 0) && (b >= 0))
                    return false;
            }
        }

        // Shitez la stanga pentru a scapa de '/'
        for(i=0; i<strlen(aux)-1; i++)
            aux[i] = aux[i+1];

        strcpy(copyF, aux+1);

        // Preiau doar expresia din paranteza
        for(i=0; i<strlen(aux)-1; i++)
        {
            if(aux[i] == ')')
            {
                aux[i+1] = NULL;
                break;
            }
        }

        // Verific daca exista puncte in intervalul [a,b] in care functia nu este definita
        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(((calculateFunction(val-step) > 0.000001) && (calculateFunction(val+step) < -0.000001)) || ((calculateFunction(val-step) < -0.000001) && (calculateFunction(val+step) > 0.000001)))
                return false;
        }
        if(((calculateFunction(b-step) > 0.000001) && (calculateFunction(b+step) < -0.000001)) || ((calculateFunction(b-step) < -0.000001) && (calculateFunction(b+step) > 0.000001)))
            return false;
        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifySqrtCondition(float a, float b, char f[])
{
    /*
        Verifica conditia de existenta a radicalului: ce este in interiorul sau trebuie sa fie >=0.
        Functia returneaza true daca nu exista radical in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care radicalul exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, "sqrt") == NULL)
        return true;

    // Preiau radicalii
    char aux[101], copyF[101];
    int i=0;
    float val;
    strcpy(copyF, f);
    while(strstr(copyF, "sqrt"))
    {
        strcpy(aux, strstr(copyF, "sqrt"));
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        // Verific daca conditia de existenta este valida (este de ajuns ca a, cea mai mica valoare, sa nu indeplineasca conditia)
        createExpression(aux);
        val = calculateFunction(a);
        if((val < 0) || (isnan(val)) || isinf(val))
            return false;

        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifyTangentCondition(float a, float b, char f[], float step)
{
    /*
        Verifica conditia de existenta a tangentei: nu este definita in punctele ((2k+1)*PI)/2
        Functia returneaza true daca nu exista functia tangenta in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care tangenta exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, "tan") == NULL)
        return true;

    char aux[101], copyF[101];
    int i=0;
    strcpy(copyF, f);
    // Preiau functiile tangente si verific conditia de existenta
    while(strstr(copyF, "tan"))
    {
        strcpy(aux, strstr(copyF, "tan"));
        i=0;
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(((calculateFunction(val-step) < -0.000001) && (calculateFunction(val+step) > 0.000001)) || ((calculateFunction(val-step) > 0.000001) && (calculateFunction(val+step) < -0.000001)))
                return false;
        }

        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifyCotangentCondition(float a, float b, char f[], float step)
{
    /*
        Verifica conditia de existenta a cotangentei: nu este definita in punctele k*PI
        Functia returneaza true daca nu exista functia cotangenta in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care cotangenta exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, "ctg") == NULL)
        return true;

    char aux[101], copyF[101];
    int i;
    strcpy(copyF, f);

    // Preiau functiile cotangente
    while(strstr(copyF, "ctg"))
    {
        strcpy(aux, strstr(copyF, "ctg"));
        i = 0;
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(((calculateFunction(val-step) < -0.000001) && (calculateFunction(val+step) > 0.000001)) || ((calculateFunction(val-step) > 0.000001) && (calculateFunction(val+step) < -0.000001)))
                return false;
        }

        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifyArcsinCondition(float a, float b, char f[], float step)
{
    /*
        Verifica conditia de existenta a arcsinusului: arcsin(x) este definita doar in intervalul [-1, 1]
        Functia returneaza true daca nu exista functia arcsinus in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care arcsinusul exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, "asin") == NULL)
        return true;

    char aux[101], copyF[101];
    int i;
    // Preiau functiile arcsinus
    strcpy(copyF, f);
    while(strstr(copyF, "asin"))
    {        strcpy(aux, strstr(copyF, "asin"));
        i=0;
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(isnan(calculateFunction(val)))
                return false;
        }
        strcpy(copyF, copyF+1);
    }
    return true;
}

bool verifyArccosCondition(float a, float b, char f[], float step)
{
    /*
        Verifica conditia de existenta a arccosinusului: arcsin(x) este definita doar in intervalul [-1, 1]
        Functia returneaza true daca nu exista functia arccosinus in functia f sau daca exista, insa conditia de existenta
    este valida.
        In cazul in care arccosinusul exista, dar conditia nu este valida, returneaza false.
    */
    if(strstr(f, "acos") == NULL)
        return true;

    char aux[101], copyF[101];
    int i;
    // Preiau functiile arcsinus
    strcpy(copyF, f);
    while(strstr(copyF, "acos"))
    {        strcpy(aux, strstr(copyF, "acos"));
        i=0;
        while(aux[i] != ')')
            i++;
        aux[i+1] = NULL;

        createExpression(aux);
        for(float val=a; val<=b; val+=step)
        {
            if(isnan(calculateFunction(val)))
                return false;
        }
        strcpy(copyF, copyF+1);
    }
    return true;
}

void mathConditions(float &a, float &b, char f[], int &nPoints, Point points[], float step)
{
    /*
        Verifica conditiile de existenta.
        In valorile unde functia nu este definita, se va pune valoarea -999999999 atat pentru x, cat si pentru y.
    */
    char aux[101], copyF[101];
    int i, coordNPoints;
    float x, copyA;

    // Verific conditia pentru radical
    if(verifySqrtCondition(a, b, f) == false)
    {
        copyA = a;
        // Preiau radicalii
        strcpy(copyF, f);
        while(strstr(copyF, "sqrt"))
        {
            strcpy(aux, strstr(copyF, "sqrt"));
            i = 0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Pun valoarea -999999999 la x si y in punctele in care functia nu este definita
            createExpression(aux);
            x = copyA;
            coordNPoints = 0;
            while((calculateFunction(x) < 0) || isnan(calculateFunction(x))|| (isinf(calculateFunction(x))))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                x+=step;
                coordNPoints++;
            }
            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru fractie
    if(verifyFractionCondition(a, b, f, step) == false)
    {
        // Preiau numitorii
        strcpy(copyF, f);
        while(strchr(copyF, '/'))
        {
            strcpy(aux, strchr(copyF, '/'));
            // Shiftez la stanga pentru a scapa de '/'
            for(i=0; i<strlen(aux)-1; i++)
                aux[i] = aux[i+1];

            if(aux[0] != '(')
                aux[1] = NULL;
            else
                // Preiau doar expresia din paranteza
                for(i=0; i<strlen(aux)-1; i++)
                {
                    if(aux[i] == ')')
                    {
                        aux[i+1] = NULL;
                        break;
                    }
                }

            // Marchez punctele in care functia nu este definita
            createExpression(aux);
            coordNPoints = 0;
            if(((calculateFunction(a-step) > 0.000001) && (calculateFunction(a+step) < -0.000001)) || ((calculateFunction(a-step) < -0.000001) && (calculateFunction(a+step) > 0.000001)))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
            }
            coordNPoints++;
            for(x=a+step; x<=b; x+=step)
            {
                if((((calculateFunction(x-step) > 0.000001) && (calculateFunction(x+step) < -0.000001)) || ((calculateFunction(x-step) < -0.000001) && (calculateFunction(x+step) > 0.000001))) && (points[coordNPoints-1].x != -999999999))
                {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                }
                coordNPoints++;
            }
            if(((calculateFunction(b-step) > 0.000001) && (calculateFunction(b+step) < -0.000001)) || ((calculateFunction(b-step) < -0.000001) && (calculateFunction(b+step) > 0.000001)))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
            }
            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru logaritm in baza 10
    if(verifyLogarithmCondition(a, b, f, step, "log") == false)
    {
        // Preiau logaritmii
        strcpy(copyF, f);
        copyA = a;
        while(strstr(copyF, "log"))
        {
            strcpy(aux, strstr(copyF, "log"));
            i=0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Calculez punctele in care logaritmul nu este definit si le marchez
            coordNPoints=0;
            createExpression(aux);
            x = copyA;
            coordNPoints = 0;
            while((isnan(calculateFunction(x))) || (calculateFunction(x) == 0) || (isinf(calculateFunction(x))))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                x+=step;
                coordNPoints++;
            }
            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru logaritm in baza 2
    if(verifyLogarithmCondition(a, b, f, step, "log2") == false)
    {
        // Preiau logaritmii
        strcpy(copyF, f);
        copyA = a;
        while(strstr(copyF, "log2"))
        {
            strcpy(aux, strstr(copyF, "log2"));
            i=0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Calculez punctele in care logaritmul nu este definit si le marchez
            coordNPoints=0;
            createExpression(aux);
            x = copyA;
            coordNPoints = 0;
            while((isnan(calculateFunction(x))) || (calculateFunction(x) == 0) || (isinf(calculateFunction(x))))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                x+=step;
                coordNPoints++;
            }
            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru logaritm in baza e
    if(verifyLogarithmCondition(a, b, f, step, "ln") == false)
    {
        // Preiau logaritmii
        strcpy(copyF, f);
        copyA = a;
        while(strstr(copyF, "ln"))
        {
            strcpy(aux, strstr(copyF, "ln"));
            i=0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Calculez punctele in care logaritmul nu este definit si le marchez
            coordNPoints=0;
            createExpression(aux);
            x = copyA;
            coordNPoints = 0;
            while(isnan(calculateFunction(x)) || (calculateFunction(x) == 0) || (isinf(calculateFunction(x))))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                x+=step;
                coordNPoints++;
            }
            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru tangenta
    if(verifyTangentCondition(a, b, f, step) == false)
    {
        // Preiau functiile tangente
        strcpy(copyF, f);
        while(strstr(copyF, "tan"))
        {
            strcpy(aux, strstr(copyF, "tan"));
            i = 0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Marchez punctele in care tangenta nu este definita
            coordNPoints = 0;
            createExpression(aux);
            for(x=a; x<=b; x+=step)
            {
                if(((calculateFunction(x-step) < -0.000001) && (calculateFunction(x+step) > 0.000001)) || ((calculateFunction(x-step) > 0.000001) && (calculateFunction(x+step) < -0.000001)))
                {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                }
                coordNPoints++;
            }
            if(((calculateFunction(b-step) < -0.000001) && (calculateFunction(b+step) > 0.000001)) || ((calculateFunction(b-step) > 0.000001) && (calculateFunction(b+step) < -0.000001)))
            {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                    coordNPoints++;
            }

            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru cotangenta
    if(verifyCotangentCondition(a, b, f, step) == false)
    {
        // Preiau functiile cotangente
        strcpy(copyF, f);
        while(strstr(copyF, "ctg"))
        {
            strcpy(aux, strstr(copyF, "ctg"));
            i = 0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Marchez punctele in care cotangenta nu este definita
            coordNPoints = 0;
            createExpression(aux);
            for(x=a; x<=b; x+=step)
            {
                if(((calculateFunction(x-step) < -0.000001) && (calculateFunction(x+step) > 0.000001)) || ((calculateFunction(x-step) > 0.000001) && (calculateFunction(x+step) < -0.000001)))
                {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                }
                coordNPoints++;
            }
            if(((calculateFunction(b-step) < -0.000001) && (calculateFunction(b+step) > 0.000001)) || ((calculateFunction(b-step) > 0.000001) && (calculateFunction(b+step) < -0.000001)))
            {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                    coordNPoints++;
            }

            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru arcsinus
    if(verifyArcsinCondition(a, b, f, step) == false)
    {
        // Preiau functiile arcsinus
        strcpy(copyF, f);
        while(strstr(copyF, "asin"))
        {
            strcpy(aux, strstr(copyF, "asin"));
            i=0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Verific punctele in care functia nu este definita si le marchez
            createExpression(aux);
            coordNPoints = 0;
            for(x=a; x<=b; x+=step)
            {
                if(isnan(calculateFunction(x)))
                {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                }
                coordNPoints++;
            }
            if(isnan(calculateFunction(b)))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                coordNPoints++;
            }

            strcpy(copyF, copyF+1);
        }
    }

    // Verific conditia pentru arccosinus
    if(verifyArccosCondition(a, b, f, step) == false)
    {
        // Preiau functiile arccosinus
        strcpy(copyF, f);
        while(strstr(copyF, "acos"))
        {
            strcpy(aux, strstr(copyF, "acos"));
            i=0;
            while(aux[i] != ')')
                i++;
            aux[i+1] = NULL;

            // Verific punctele in care functia nu este definita si le marchez
            createExpression(aux);
            coordNPoints = 0;
            for(x=a; x<=b; x+=step)
            {
                if(isnan(calculateFunction(x)))
                {
                    points[coordNPoints].x = -999999999;
                    points[coordNPoints].y = -999999999;
                }
                coordNPoints++;
            }
            if(isnan(calculateFunction(b)))
            {
                points[coordNPoints].x = -999999999;
                points[coordNPoints].y = -999999999;
                coordNPoints++;
            }

            strcpy(copyF, copyF+1);
        }
    }
}


#endif // MATHONDITIONS_H
