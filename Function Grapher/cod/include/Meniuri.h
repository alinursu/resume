#ifndef MENIURI_H
#define MENIURI_H

#include<InputBoxes.h>
#include <list>

#include "../lib/mainGraph.h"

#define WIDTH 750
#define HEIGHT 750

list<button> activeButtons;
string functie, stg, drp;
int culoare = WHITE;

int c1 = WHITE;
int c2 = COLOR(235, 129, 129); // rosu
int c3 = COLOR(125, 138, 227); // albastru
int c4 = COLOR(230, 227, 142); // galben
int c5 = COLOR(219, 124, 230); // mov
int c6 = COLOR(156, 240, 227); // cyan

int spatiuIntreCasute = 40;
int laturaCasute = 70;
int startXCasute = 40;
int startYCasute = 530;

char func_char[100], stg_char[10], drp_char[10];

list<button> deseneazaPATTERN()
{
    cleardevice();

    list<button> active;

    active.push_back(
    createButton(0, 0, 0, 0, "id", "Text", 1)
    );

    return active;
}

list<button> deseneazaMeniuPrincipal()
{
    cleardevice();

    list<button> active;

    // TITLUL APLICATIEI
    char titlu[] = "Graficul Functiei";
    settextstyle(BOLD_FONT, HORIZ_DIR, 7);
    settextjustify(CENTER_TEXT, CENTER_TEXT);
    outtextxy(WIDTH/2, HEIGHT/3, titlu);

    // Butonul de Start
    //setcolor(COLOR(66, 135, 245));
    active.push_back(
    createButton(WIDTH / 2, HEIGHT / 2, 170, 70, "start", "Start", 5)
    );

    // Butonul de Despre
    active.push_back(
    createButton(WIDTH / 2, HEIGHT / 2 + 100, 170, 70, "despre", "Despre", 5)
    );
    // Text numele studentilor
    settextstyle(BOLD_FONT, HORIZ_DIR, 3);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(455, 680, "Proiect realizat de:");
    settextstyle(BOLD_FONT, HORIZ_DIR, 2);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(565, 700, "Chiriac Victor");
    outtextxy(540, 720, "Ursu Stefan-Alin");
    outtextxy(410, 740, "Grupa B4, Anul I, 2019-2020");
    return active;
}

list<button> deseneazaMeniuInput()
{
    cleardevice();

    list<button> active;

    // Butonul de intoarcere la meniul principal
    active.push_back(
    createButton(50, 25, 90, 40, "paginaPrincipala", "Inapoi", 3)
    );

    // Text input functie
    settextstyle(BOLD_FONT, HORIZ_DIR, 4);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(10, 150, "f(x)=");

    // Casuta input functie
    int xaux = 115;
    active.push_back(
    createButtonTopLeft(115, 120, 600, 40, "inputFunctie", "", 6)
    );


    // Text input domeniu functie
    settextstyle(BOLD_FONT, HORIZ_DIR, 4);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(10, 300, "Domeniu");
    settextstyle(BOLD_FONT, HORIZ_DIR, 5);

    outtextxy(10, 400, "f:(");
    // Casuta input limita stanga
    active.push_back(
    createButtonTopLeft(100, 370, 85, 40, "limitaStanga", "", 4)
    );

    settextstyle(BOLD_FONT, HORIZ_DIR, 5);
    outtextxy(200, 400, ",");
    // Casuta input limita dreapta
    active.push_back(
    createButtonTopLeft(215, 370, 85, 40, "limitaDreapta", "", 4)
    );
    // Restul textului pentru a defini domeniul
    settextstyle(BOLD_FONT, HORIZ_DIR, 5);
    outtextxy(400, 400, ") -> |R");

    // Input de culoare
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    settextstyle(BOLD_FONT, HORIZ_DIR, 4);
    outtextxy(10, 500, "Culoare");
    settextstyle(BOLD_FONT, HORIZ_DIR, 5);

    // Casute input culoare
    setlinestyle(SOLID_LINE, 1, THICK_WIDTH);
    active.push_back(
    createFillButtonTopLeft(startXCasute, startYCasute, laturaCasute, laturaCasute, "c1", "", 2, c1)
    );
    active.push_back(
    createFillButtonTopLeft(startXCasute + laturaCasute + spatiuIntreCasute, startYCasute, laturaCasute, laturaCasute, "c2", "", 2, c2)
    );
    active.push_back(
    createFillButtonTopLeft(startXCasute + laturaCasute * 2 + spatiuIntreCasute * 2, startYCasute, laturaCasute, laturaCasute, "c3", "", 2, c3)
    );
    active.push_back(
    createFillButtonTopLeft(startXCasute + laturaCasute * 3 + spatiuIntreCasute * 3, startYCasute, laturaCasute, laturaCasute, "c4", "", 2, c4)
    );
    active.push_back(
    createFillButtonTopLeft(startXCasute + laturaCasute * 4 + spatiuIntreCasute * 4, startYCasute, laturaCasute, laturaCasute, "c5", "", 2, c5)
    );
    active.push_back(
    createFillButtonTopLeft(startXCasute + laturaCasute * 5 + spatiuIntreCasute * 5, startYCasute, laturaCasute, laturaCasute, "c6", "", 2, c6)
    );

    setlinestyle(SOLID_LINE, 1, NORM_WIDTH);
    // Butonul ce trimite spre pagina graficului
    active.push_back(
    createButtonTopLeft(490, 660, 210, 50, "spreGrafic", "Genereaza!", 4)
    );

    // Umple cu date deja existente in cazul in care se intoarce din desenarea graficului

    settextjustify(LEFT_TEXT, CENTER_TEXT);
    settextstyle(BOLD_FONT, HORIZ_DIR, 3);
    char auxText[100];
    strcpy(auxText, functie.c_str());
    outtextxy(123, 148, auxText); // functia
    strcpy(auxText, stg.c_str());
    outtextxy(105, 395, auxText); // limita stanga
    strcpy(auxText, drp.c_str());
    outtextxy(220, 395, auxText); // limita dreapta
    // Highlight culoare activa
    if(culoare != 0)
    {
        int deInmultitSpatii = 0;
        if(culoare == c2)
            deInmultitSpatii = 1;
        else if(culoare == c3)
            deInmultitSpatii = 2;
        else if(culoare == c4)
            deInmultitSpatii = 3;
        else if(culoare == c5)
            deInmultitSpatii = 4;
        else if(culoare == c6)
            deInmultitSpatii = 5;

        setlinestyle(SOLID_LINE, 1, THICK_WIDTH);
        createChenarTopLeft(startXCasute + deInmultitSpatii * laturaCasute + deInmultitSpatii * spatiuIntreCasute, startYCasute, laturaCasute, laturaCasute, COLOR(255,0,0));
        setlinestyle(SOLID_LINE, 1, NORM_WIDTH);
    }

    return active;
}

list<button> deseneazaMeniuGrafic()
{
    cleardevice();

    list<button> active;

    // Butonul de intoarcere la meniul principal
    active.push_back(
    createButton(50, 25, 90, 40, "start", "Inapoi", 3)
    );

    // Codul care deseneaza graficul
    strcpy(func_char, functie.c_str());
    strcpy(stg_char, stg.c_str());
    strcpy(drp_char, drp.c_str());
    drawGraph(func_char, convertCharToFloat(stg_char), convertCharToFloat(drp_char), culoare);

    return active;
}

list<button> deseneazaMeniuDespre()
{
    cleardevice();

    list<button> active;

    // Butonul de intoarcere la meniul principal
    active.push_back(
    createButton(50, 25, 90, 40, "paginaPrincipala", "Inapoi", 3)
    );

    // Titlu pagina despre
    settextstyle(BOLD_FONT, HORIZ_DIR, 6);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(290, 80, "Despre");

    // Text despre
    settextstyle(BOLD_FONT, HORIZ_DIR, 3);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(20, 150, "Operatii, functii si constante disponibile: ");

    // Text pagina despre
    settextstyle(BOLD_FONT, HORIZ_DIR, 2);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(70, 185, "+ (Adunarea)");
    outtextxy(70, 205, "- (Scaderea)");
    outtextxy(70, 225, "* (Inmultirea)");
    outtextxy(70, 245, "/ (Impartirea)");
    outtextxy(70, 265, "^ (Functia putere)");
    outtextxy(70, 285, "% (Modulo)");
    outtextxy(70, 305, "log() (Logaritm in baza 10)");
    outtextxy(70, 325, "log2() (Logaritm in baza 2)");
    outtextxy(70, 345, "ln() (Logaritm natural)");
    outtextxy(70, 365, "sqrt() (Functia radical)");
    outtextxy(70, 385, "abs() (Functia absolut)");
    outtextxy(70, 405, "sin() (Functia sinus)");
    outtextxy(70, 425, "cos() (Functia cosinus)");
    outtextxy(70, 445, "tan() (Functia tangenta)");
    outtextxy(70, 465, "ctg() (Functia cotangenta)");
    outtextxy(70, 485, "asin() (Functia arcsinus)");
    outtextxy(70, 505, "acos() (Functia arccosinus)");
    outtextxy(70, 525, "atan() (Functia arctangenta)");
    outtextxy(70, 545, "actg() (Functia arccotangenta");
    outtextxy(70, 565, "E (Numarul lui Euler; E~2.71828)");
    outtextxy(70, 585, "PI (Constanta PI; PI~3.14159)");
    outtextxy(70, 605, "INF (Un numar foarte mare)");
    outtextxy(70, 625, "-INF (Un numar foarte mic)");

    // Text numele studentilor
    settextstyle(BOLD_FONT, HORIZ_DIR, 3);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(455, 680, "Proiect realizat de:");
    settextstyle(BOLD_FONT, HORIZ_DIR, 2);
    settextjustify(LEFT_TEXT, CENTER_TEXT);
    outtextxy(565, 700, "Chiriac Victor");
    outtextxy(540, 720, "Ursu Stefan-Alin");
    outtextxy(410, 740, "Grupa B4, Anul I, 2019-2020");

    return active;
}

// evaluareExpression(getExpressionTree())

#endif // MENIURI_H
