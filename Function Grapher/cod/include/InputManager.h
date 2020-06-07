#ifndef INPUTMANAGER_H
#define INPUTMANAGER_H

#include <Meniuri.h>

#include <windows.h>
#include <cstring>
#include <conio.h>
#include <list>
using namespace std;

void assignString(string res, string id)
{
    if(id == "inputFunctie")
        functie = res;
    else if(id == "limitaStanga")
        stg = res;
    else if(id == "limitaDreapta")
        drp = res;
}

button getButton(string id)
{
    for(list<button>::iterator it = activeButtons.begin(); it != activeButtons.end(); ++it)
        if(it->id == id)
            return *it;
}

bool eCaracterDeFinal(char c)
{
    if(c == 13) // Enter
        return 1;
    if(c == 27) // Esc
        return 1;

    return 0;
}
bool eCaracterInterzis(char c)
{
    if(c == 0)
        return 1;
    return 0;
}
void clearTextBox(string id)
{
    int points[8];

    button aux = getButton(id);
    int margin = 2;

    points[0] = aux.xStart + margin;
    points[1] = aux.yStart + margin;
    points[2] = aux.xEnd - margin;
    points[3] = aux.yStart + margin;
    points[4] = aux.xEnd - margin;
    points[5] = aux.yEnd - margin;
    points[6] = aux.xStart + margin;
    points[7] = aux.yEnd - margin;

    setcolor(BLACK);
    setfillstyle(SOLID_FILL, BLACK);
    fillpoly(4, points);

    setcolor(WHITE);
}

string inputStream(string id)
{
    int xOut=0, yOut=0, textSize=0, maxSize = 0;

    if(id == "inputFunctie")
    {
        xOut = 123;
        yOut = 148;
        textSize = 3;
        maxSize = 42;
    }
    else if(id == "limitaStanga")
    {
        xOut = 105;
        yOut = 395;
        textSize = 3;
        maxSize = 5;
    }
    else if(id == "limitaDreapta")
    {
        xOut = 220;
        yOut = 395;
        textSize = 3;
        maxSize = 5;
    }

    string input;

    settextjustify(LEFT_TEXT, CENTER_TEXT);
    settextstyle(BOLD_FONT, HORIZ_DIR, textSize);

    char c = getch();
    while(!eCaracterDeFinal(c))
    {
        if(!eCaracterInterzis(c))
        {
            if(c == 8){ // Backspace, elimina ultimul caracter
            if(input.size() > 0)
                input.pop_back();
            }
            else if(input.size() < maxSize)
                input += c;
            // Modifica text box-ul sa apara caracterul

            char inputAsArray[100];
            strcpy(inputAsArray, input.c_str()); // Transforma string-ul in sir de caractere

            clearTextBox(id);
            outtextxy(xOut, yOut, inputAsArray);
        }

        c = getch();
    }

    cout << input << endl;
    return input;
}

void apasaButon(string id)
{
    button aux = getButton(id);
    // Functia defineste actiunea pe care o face butonul apasat cu id-ul din parametru
    if(id == "start")
    {
        activeButtons = deseneazaMeniuInput();
    } else

    if(id == "despre")
    {
        activeButtons = deseneazaMeniuDespre();
    } else

    if(id == "paginaPrincipala")
    {
        activeButtons = deseneazaMeniuPrincipal();
    } else

    if(id == "spreGrafic")
    {
        bool ok = 1;

        button aux;
        if(functie == ""){
            // Border rosu functie
            aux = getButton("inputFunctie");
            createChenarTopLeft(aux.xStart, aux.yStart, aux.xEnd - aux.xStart, aux.yEnd - aux.yStart, COLOR(255, 0, 0));
            ok = 0;
        }
        if(stg == ""){
            // Border rosu limita stanga
            aux = getButton("limitaStanga");
            createChenarTopLeft(aux.xStart, aux.yStart, aux.xEnd - aux.xStart, aux.yEnd - aux.yStart, COLOR(255, 0, 0));
            ok = 0;
        }
        if(drp == ""){
            // Border rosu limita dreapta
            aux = getButton("limitaDreapta");
            createChenarTopLeft(aux.xStart, aux.yStart, aux.xEnd - aux.xStart, aux.yEnd - aux.yStart, COLOR(255, 0, 0));
            ok = 0;
        }
        if(ok)
            activeButtons = deseneazaMeniuGrafic();

        cout << functie << ' ' << stg << ' ' << drp << endl;
    } else

    if(id == "c1" || id == "c2" || id == "c3" || id == "c4" || id == "c5" || id == "c6")
    {
        // Pune border alb la toate din nou
        setlinestyle(SOLID_LINE, 1, THICK_WIDTH);
        for(int x = startXCasute, i = 1; i <= 6; i++, x = x + laturaCasute + spatiuIntreCasute)
            createChenarTopLeft(x, startYCasute, laturaCasute, laturaCasute, WHITE);

        // Pune border rosu la cel selectat
        int deInmultitSpatii = 0;
        if(id == "c1")
            culoare = c1;
        else if(id == "c2")
            culoare = c2, deInmultitSpatii = 1;
        else if(id == "c3")
            culoare = c3, deInmultitSpatii = 2;
        else if(id == "c4")
            culoare = c4, deInmultitSpatii = 3;
        else if(id == "c5")
            culoare = c5, deInmultitSpatii = 4;
        else
            culoare = c6, deInmultitSpatii = 5;

        setlinestyle(SOLID_LINE, 1, THICK_WIDTH);
        createChenarTopLeft(startXCasute + deInmultitSpatii * laturaCasute + deInmultitSpatii * spatiuIntreCasute, startYCasute, laturaCasute, laturaCasute, COLOR(255,0,0));
        setlinestyle(SOLID_LINE, 1, NORM_WIDTH);
    }
    else {
        // Textbox-uri
        createChenarTopLeft(aux.xStart, aux.yStart, aux.xEnd - aux.xStart, aux.yEnd - aux.yStart, COLOR(255, 175, 175));
        clearTextBox(id);
        string result = inputStream(id);
        assignString(result, id);
        createChenarTopLeft(aux.xStart, aux.yStart, aux.xEnd - aux.xStart, aux.yEnd - aux.yStart, WHITE);
   }
}

bool apasatInButon(int x, int y, button b)
{
    // Verifica daca punctul (x, y) se afla in buton
    if(b.xStart <= x && x <= b.xEnd &&
       b.yStart <= y && y <= b.yEnd)
       {
            PlaySound("BUTTON_PRESS.wav", NULL, SND_FILENAME);
            return 1;
       }

    return 0;
}

void verificaApasare(int x, int y)
{
    // Trece prin lista cu butoanele active din scena curenta
    for(list<button>::iterator it = activeButtons.begin(); it != activeButtons.end(); ++it)
        if(apasatInButon(x, y, *it))
            apasaButon(it->id);

}

#endif // INPUTMANAGER_H
