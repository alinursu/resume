#include "scaleAndStep.h"
#include "dataConversions.h"
#include <cmath>
#include <iostream>

#define NUMBERPOINTS 750
using namespace std;

struct Point{
    float x;
    float y;
};

void setStep(float a, float b, float &step)
{
    /*
        Calculeaza valoarea pasului astfel incat, in intervalul [a,b], sa se faca exact NUMBERPOINTS pasi.
    */
    if((b<0) && (a<0))
        step = (abs(b) + abs(a))/NUMBERPOINTS;
    else if(a<0)
        step = (b-a)/NUMBERPOINTS;
    else if(a>0)
        step = (b+a)/NUMBERPOINTS;
}

void setScaleY(float &maxValueOfFunction, int nPoints, Point points[], float &signedMin, float &signedMax)
{
    /*
        Calculeaza o scara pentru valorile codomeniului astfel incat graficul sa nu iasa inafara ariei axelor si, in
    acelasi timp, sa nu fie nici prea mic.
    */

    float difference, percent;
    if(maxValueOfFunction < 300)
    {
        // Graf prea restrans, il mai largesc
        difference = 300 - maxValueOfFunction;
        percent = (difference*100)/maxValueOfFunction;
        maxValueOfFunction = 300;
        signedMin = signedMin + percent/100*signedMin;
        signedMax = signedMax + percent/100*signedMax;
        for(int i=0; i<nPoints; i++)
            points[i].y = points[i].y + percent/100 * points[i].y;
    }
    else if(maxValueOfFunction > 300)
    {
        // Graf care depaseste aria axelor, in special in partea pozitiva
        difference = maxValueOfFunction - 300;
        percent = (difference*100)/maxValueOfFunction;
        maxValueOfFunction = 300;
        signedMin = signedMin - percent/100 * signedMin;
        signedMax = signedMax - percent/100 * signedMax;
        for(int i=0; i<nPoints; i++)
            points[i].y = points[i].y - percent/100 * points[i].y;
    }
    else if(maxValueOfFunction < -300)
    {
        // Graf care depaseste aria axelor, in special in partea negativa
        difference = abs(maxValueOfFunction) - 300;
        percent = (difference*100)/abs(maxValueOfFunction);
        maxValueOfFunction = -300;
        signedMin = signedMin + percent/100*abs(signedMin);
        signedMax = signedMax + percent/100*abs(signedMax);
        for(int i=0; i<nPoints; i++)
            points[i].y = points[i].y + percent/100*abs(points[i].y);
    }
}

void setScaleX(int nPoints, Point points[], float &a, float &b)
{
    /*
        Calculeaza o scara pentru valorile din domeniu astfel incat graful sa nu iasa din aria axelor si, in acelasi timp,
    sa nu fie nici prea mic.
    */
    float difference, percent;
    float maxX;
    maxX = max(abs(a), abs(b));
    if(maxX < 150)
    {
        // Graf prea restrans, il mai largesc
        if(maxX == abs(a))
        {
            difference = 300 - abs(a);
            percent = (difference*100)/abs(a);
            a = -300;
            if(b > 0)
                b = b + percent/100*abs(b);
            else
                b = b - percent/100*abs(b);
        }
        else if(maxX == abs(b))
        {
            difference = 300 - abs(b);
            percent = (difference*100)/abs(b);
            b = 300;
            if(a > 0)
                a = a + percent/100*abs(a);
            else
                a = a - percent/100*abs(a);
        }
        for(int i=0; i<nPoints; i++)
            if(points[i].x > 0)
                points[i].x = points[i].x + percent/100*abs(points[i].x);
            else
                points[i].x = points[i].x - percent/100*abs(points[i].x);
    }
    else if(maxX == abs(a))
    {
        if(a < -300)
        {
            // Graf care depaseste aria axelor in partea lui a, cea negativa
            difference = abs(a) - 300;
            percent = (difference*100)/abs(a);
            a = -300;
            b = b - percent/100 * abs(b);
            for(int i=0; i<nPoints; i++)
                if(points[i].x < 0)
                    points[i].x = points[i].x + percent/100 * abs(points[i].x);
                else
                    points[i].x = points[i].x - percent/100 * abs(points[i].x);
        }
    }
    else if(maxX == abs(b))
    {
        if(b > 300)
        {
            // Graf care depaseste aria axelor in partea lui b, cea pozitiva
            difference = b - 300;
            percent = (difference*100)/b;
            b = 300;
            if(a < 0)
                a = a + percent/100 * abs(a);
            else
                a = a - percent/100 * abs(a);
            for(int i=0; i<nPoints; i++)
                if(points[i].x > 0)
                    points[i].x = points[i].x - percent/100 * abs(points[i].x);
                else
                    points[i].x = points[i].x + percent/100 * abs(points[i].x);
        }
    }
}
