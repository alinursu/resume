#include <stdlib.h>
#include <stdio.h>
#include <math.h>
using namespace std;

struct Variables { // O lista care va memora toate variabilele expresiei
    char* name; // Numele variabilei
    double value;  // Valoarea variabilei
    Variables* next; // Pointer catre urmatoarea variabila

    Variables(char* name, double value):name(name), value(value), next(NULL) {}
}*vars;

void addVariable(Variables* &vars, char* name, double value) {
	// functie pentru a aduga o variabila noua in lista de variabile
    Variables* newVar = new Variables(name, value);

    if (vars == NULL) {
        vars = newVar;
        return;
    }

    Variables* tempVar = vars;
    while(tempVar->next)
        tempVar = tempVar->next;
    tempVar->next = newVar;
}

void resetVariables(Variables* &vars) {
	// Sterge toate valorile si variabilele
    Variables* temp = vars;
    while(temp != NULL) {
        temp = vars->next;
        delete(vars);
        vars = temp;
    }
}

void drawVariables(Variables* &vars, int x, int y) {
	// Deseneaza variabilele pe ecran
    Variables* p = vars;
    char text[50];
    int i = 0;
    while(p) {
        sprintf(text, "%s = %f", p->name, p->value);
        outtextxy(x, y+i*(textheight(text)+5), text);
        i++;
        p = p->next;
    }
}

double getVariableValue(Variables* &vars, char name[]) {
	// Returneaza valoarea variabilei in caz ca o gaseste,iar in caz contrar va pune utilizatorul sa dea o valoare variabilei respective
    bool ok;
    double value;

    Variables* tempVar = vars;
    while (tempVar) {
        if (!strcmp(tempVar->name, name))
            return tempVar->value;
        tempVar = tempVar->next;
    }

    do {
        if (!strcmp(name, "PI")) {
            value = PI; // constanta pi
            addVariable(vars, name, value);
            ok = 1;
        } else if (!strcmp(name, "E")) {
            value = E; // constanta euler
            addVariable(vars, name, value);
            ok = 1;
        } else {
            return NAN; // Not A Number, reprezinta faptul ca variabila nu a fost initializata inainte
        }
    } while (ok == 0);

    return value;
}

bool isVariableSet(Variables* &vars, char name[]) {
	// Verifica daca o variabila este initializata
    if(isnan(getVariableValue(vars, name)))
        return false;
    return true;
}
