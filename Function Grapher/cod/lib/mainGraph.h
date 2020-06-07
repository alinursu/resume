#ifndef MAIN2_H
#define MAIN2_H

#include <iostream>
#include <cmath>
#include <winbgim.h>
#include <graphics.h>
#include <cstring>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "scaleAndStep.h"
#include "dataConversions.h"
#include "mainLib.h"
#include "mathConditions.h"

#define WIDTH 750
#define HEIGHT 750

#define DELAY 1

using namespace std;

char f[101];
float a, b, copyA, copyB;
char stra[15], strb[15];
int root;
float step = 0.01;
float maxValueOfFunction, signedMaxValueOfFunction, signedMinValueOfFunction, copySignedMax, copySignedMin;

Point points[1000001];
int nPoints;

void clearPointsArray()
{
    /*
        Goleste vectorul points si seteaza ca fiind 0 valoarea lui nPoints.
    */
    for(int i=0; i<nPoints; i++)
        points[i].x = points[i].y = 0;
    nPoints = 0;
}

void drawGraph(char f[], float a, float b, int color)
{
    // Desenez grid-ul din 25 in 25 px
    setcolor(COLOR(80, 80, 80));
    int coordGrid = 25;
    int it = 1;
    while(coordGrid < 750)
    {
        int posX = 0, posY = 0;

        if(it <= 3)
            posY = 50;

        if(it <= 1)
            posX = 100;

        line(coordGrid, posY, coordGrid, HEIGHT);
        line(posX, coordGrid, WIDTH, coordGrid);

        coordGrid+=25;
        it++;
    }
    setcolor(WHITE);

    // Setez font-ul
    settextstyle(BOLD_FONT, HORIZ_DIR, 1);
    settextjustify(LEFT_TEXT, CENTER_TEXT);

    // Golesc points
    clearPointsArray();

    // Verific conditia a <= b
    if(a > b)
        swap(a, b);
    // Transform expresia data la intrare intr-o forma in care se poate calcula
    createExpression(f);

    // Redesenez axele Ox si Oy
    line(50, int(HEIGHT/2), WIDTH-50, int(HEIGHT/2));
    line(int(WIDTH/2), 50, int(WIDTH/2), HEIGHT-50);
    line(int(WIDTH/2)-10, 60, int(WIDTH/2), 50);
    line(WIDTH-60, HEIGHT/2-10, WIDTH-50, HEIGHT/2);
    line(WIDTH-50, HEIGHT/2, WIDTH-60, HEIGHT/2+10);
    line(int(WIDTH)/2, 50, int(WIDTH/2)+10, 60);

    // Evidentiez Originea si axele
    outtextxy(int(WIDTH/2)+5, int(HEIGHT/2)-10, "O(0,0)");
    outtextxy(WIDTH/2+5, 45, "x");
    outtextxy(WIDTH-45, HEIGHT/2-10, "y");

    // Calculez pasul
    setStep(a, b, step);

    // Verific conditiile de existenta
    mathConditions(a, b, f, nPoints, points, step);

    // Transform expresia data la intrare intr-o forma in care se poate calcula
    createExpression(f);

    // Calculez punctele graficului in intervalul [a,b], cu pasul step
    if(points[0].x != -999999999)
    {
        maxValueOfFunction = abs(calculateFunction(a));
        signedMaxValueOfFunction = calculateFunction(a);
        signedMinValueOfFunction = calculateFunction(a);
    }
    else
    {
        maxValueOfFunction = -999999999;
        signedMaxValueOfFunction = -999999999;
        signedMinValueOfFunction = -999999999;
    }
    float auxVal = a;
    while(points[nPoints].x != 0)
    {
        auxVal += step;
        nPoints++;
    }
    for(float val=auxVal; val<=b; val+=step)
    {
        if(points[nPoints].x != -999999999)
        {
            if((abs(calculateFunction(val)) > maxValueOfFunction) || (maxValueOfFunction == -999999999))
                maxValueOfFunction = abs(calculateFunction(val));
            if(((calculateFunction(val) > signedMaxValueOfFunction) || (signedMaxValueOfFunction) == -999999999))
                signedMaxValueOfFunction = calculateFunction(val);
            if((calculateFunction(val) < signedMinValueOfFunction) || (signedMinValueOfFunction == -999999999))
                signedMinValueOfFunction = calculateFunction(val);
            points[nPoints].x = val;
            points[nPoints].y = calculateFunction(val);
        }
        nPoints++;
    }
    if(points[nPoints-1].x != b)
    {
        // Cateodata nu ajunge chiar in capat din cauza step-ului care depaseste b-ul
        if(points[nPoints].x != -999999999)
        {
            points[nPoints].x = b;
            points[nPoints].y = calculateFunction(b);
            if((abs(points[nPoints].y) > maxValueOfFunction) || (maxValueOfFunction == -999999999))
                maxValueOfFunction = abs(points[nPoints].y);
            if((points[nPoints].y > signedMaxValueOfFunction) || (signedMaxValueOfFunction == -999999999))
                signedMaxValueOfFunction = points[nPoints].y;
            if((points[nPoints].y < signedMinValueOfFunction) || (signedMinValueOfFunction == -999999999))
                signedMinValueOfFunction = points[nPoints].y;
        }
        nPoints++;
    }

    // Setez scara si fac copii ale variabilelor ce vor fi afisate pe graf
    copyA = a;
    copyB = b;
    copySignedMax = signedMaxValueOfFunction;
    copySignedMin = signedMinValueOfFunction;
    copyA = onlyThreeDigits(copyA);
    copyB = onlyThreeDigits(copyB);
    copySignedMax = onlyThreeDigits(copySignedMax);
    copySignedMin = onlyThreeDigits(copySignedMin);
    setScaleY(maxValueOfFunction, nPoints, points, signedMinValueOfFunction, signedMaxValueOfFunction);
    setScaleX(nPoints, points, a, b);

    // Afisez valorile domeniului si codomeniului functiei pe grafic
    if(copyA != 0)
    {
        line(WIDTH/2+a, HEIGHT/2-5, WIDTH/2+a, HEIGHT/2+5);
        outtextxy(WIDTH/2+a-10, HEIGHT/2+25, convertFloatToChar(copyA));
    }
    if(copyB != 0)
    {
        line(WIDTH/2+b, HEIGHT/2-5, WIDTH/2+b, HEIGHT/2+5);
        outtextxy(WIDTH/2+b-10, HEIGHT/2+25, convertFloatToChar(copyB));
    }
    if(copySignedMin != 0)
    {
        line(WIDTH/2-5, HEIGHT/2-signedMinValueOfFunction, WIDTH/2+5, HEIGHT/2-signedMinValueOfFunction);
        outtextxy(WIDTH/2+10, HEIGHT/2-signedMinValueOfFunction+5, convertFloatToChar(copySignedMin));
    }
    if(copySignedMax != 0)
    {
        line(WIDTH/2-5, HEIGHT/2-signedMaxValueOfFunction, WIDTH/2+5, HEIGHT/2-signedMaxValueOfFunction);
        outtextxy(WIDTH/2+10, HEIGHT/2-signedMaxValueOfFunction+5, convertFloatToChar(copySignedMax));
    }

    // Afisez punctele, unindu-le intre ele cu linii
    // SETAREA CULORII PENTRU GRAF APARE AICI
    setcolor(color);
    for(int i=1; i<nPoints; i++)
    {
        if((points[i-1].x != -999999999) && (points[i].x != -999999999))
        {
            if(DELAY)
                delay(1);
            line(WIDTH/2 + points[i-1].x, HEIGHT/2 - points[i-1].y, WIDTH/2 + points[i].x, HEIGHT/2 - points[i].y);
        }
        else if((points[i-1].x == -999999999) && (points[i].x == -999999999))
            continue;
        else if(points[i-1].x == -999999999)
            continue;
        else if(points[i].x == -999999999)
        {
            int copyI = i-1;
            while(points[i].x == -999999999)
                i++;
            if(DELAY)
                delay(1);
            line(WIDTH/2 + points[copyI].x, HEIGHT/2 - points[copyI].y, WIDTH/2 + points[i].x, HEIGHT/2 - points[i].y);
        }
    }
    setcolor(WHITE);
}


#endif // MAIN2_H
