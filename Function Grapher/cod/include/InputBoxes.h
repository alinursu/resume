#ifndef INPUTBOXES_H
#define INPUTBOXES_H

#include <string>
using namespace std;

struct button
{
    int xStart, yStart; // Pozitia pe ecran
    int xEnd, yEnd;
    string id; // Id dupa care va fi gasit in functia apasaButon()
};

button createButton(int centruX, int centruY, int lungime, int inaltime, string id, char text[], int textMarime)
{
    // Scrisul din interior
    settextstyle(BOLD_FONT, HORIZ_DIR, textMarime);
    settextjustify(CENTER_TEXT, CENTER_TEXT);
    outtextxy(centruX, centruY + 5, text);
    // Chenarul
    rectangle(centruX - lungime / 2, centruY - inaltime / 2, centruX + lungime / 2, centruY + inaltime / 2);
    button aux = {centruX - lungime / 2, centruY - inaltime / 2, centruX + lungime / 2, centruY + inaltime / 2, id};

    return aux;
}

button createButtonTopLeft(int topLeftX, int topLeftY, int width, int height, string id, char text[], int textMarime)
{
    // Utilizeaza functia createButton pentru a crea un buton avand coordonatele coltului sus stanga
    return createButton(topLeftX + width / 2, topLeftY + height / 2, width, height, id, text, textMarime);
}

button createFillButtonTopLeft(int topLeftX, int topLeftY, int width, int height, string id, char text[], int textMarime, int color)
{
    button aux = createButton(topLeftX + width / 2, topLeftY + height / 2, width, height, id, text, textMarime);
    setfillstyle(SOLID_FILL, color);
    floodfill(topLeftX + width / 2, topLeftY + height / 2, WHITE);

    return aux;
}

void createChenar(int centruX, int centruY, int lungime, int inaltime, int color)
{
    // Creaza un chenar patratic de culoarea color
    setcolor(color);
    rectangle(centruX - lungime / 2, centruY - inaltime / 2, centruX + lungime / 2, centruY + inaltime / 2);
    setcolor(WHITE);
}

void createChenarTopLeft(int topLeftX, int topLeftY, int lungime, int inaltime, int color)
{
    // Utilizeaza functia createChenar pentru a crea un chenar avand coordonatele coltului sus stanga
    createChenar(topLeftX + lungime / 2, topLeftY + inaltime / 2, lungime, inaltime, color);
}

#endif // INPUTBOXES_H
