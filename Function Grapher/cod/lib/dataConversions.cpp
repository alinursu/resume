#include "dataConversions.h"
#include <cstring>
#include <cmath>
using namespace std;

#define INF 9999
#define PI 3.14159
#define E 2.71828

bool verifyIfItsValidFloat(char *number)
{
    /*
        Verific daca un sir de caractere reprezinta un numar sau nu.

        Exemple:
            58932 => return true;
            -37821 => return true;
            3.812 => return true;
            3,812 => return false;
            8378a21 => return false;
    */
    if((number[0] != '-') && (strchr("0123456789.", number[0]) == NULL))
        return false;
    for(int i=1; i<strlen(number); i++)
        if(strchr("0123456789.", number[i]) == NULL)
            return false;
    return true;
}

int power(int n, int p)
{
    /*
        Calculeaza n^p in timp logaritmic.
    */
    if((p==0) || (n==1))
        return 1;
    if(p==1)
        return n;
    if(p%2 == 0)
        return power(n*n, p/2);
    return n*power(n*n, (p-1)/2);
}

int reverseInt(int x)
{
    /*
        Returneaza inversul unui numar intreg.
    */
    int rX=0;
    while(x != 0)
    {
        rX = rX*10 + x%10;
        x /= 10;
    }
    return rX;
}

char* convertFloatToChar(float x)
{
    /*
        Returneaza un pointer char care contine valoarea lui x.
        Exemple:
            convertFloatToChar(3.1418) => "3.1418"
            convertFloatToChar(50) => "50"
    */
    char* v = new char[51];
    int nV = 0;

    // Verific daca exista minus
    if(x < 0)
    {
        v[nV] = '-';
        nV++;
        x = abs(x);
    }

    // Partea intreaga
    int integerX = int(x);
    int pow10=0;
    x = x - integerX;

    if(integerX == 0)
    {
        v[nV] = '0';
        nV++;
    }
    else
    {
        while((integerX%10 == 0) && (integerX != 0))
        {
            pow10++;
            integerX/=10;
        }

        integerX = reverseInt(integerX);
        while(integerX != 0)
        {
            v[nV] = integerX%10 + '0';
            nV++;
            integerX /= 10;
        }

        while(pow10 != 0)
        {
            v[nV] = '0';
            nV++;
            pow10--;
        }
    }

    // Partea fractionara
    if(x != 0)
    {
        v[nV] = '.';
        nV++;
        int digits = 0;
        while((x > 0) && (digits < 3))
        {
            x *= 10;
            v[nV] = int(x)%10 + '0';
            nV++;
            x = x - int(x);
            digits++;
        }
    }
    v[nV] = NULL;
    return v;
}

int lengthOfIntegerPart(float x)
{
    /*
        Calculeaza numarul de cifre din partea intreaga a lui x.
        ex: 1234,567 => return 4;
    */
    int n=0;
    int intx = (int)x;
    while(intx != 0)
    {
        n++;
        intx /= 10;
    }
    return n;
}

float convertCharToFloat(char *number)
{
    /*
        Converteste un sir de caractere ce reprezinta un numar intr-o data de tip intreg.
    */

    // Verific daca number este +/-INF
    if(strstr(number, "INF"))
    {
        if((strlen(number) == 3) || (strlen(number) == 4))
        {
            if(number[0] == '-')
                return -INF;
            else
                return INF;
        }
        else
        {
            char op;
            if(number[0] == '-')
                op = number[4];
            else
                op = number[3];

            if(number[0] == '-')
            {
                if(op == '+')
                    return -INF + (int(number[5]) - '0');
                else if(op == '-')
                    return -INF - (int(number[5]) - '0');
                else if(op == '*')
                    return -INF * (int(number[5]) - '0');
                else if(op == '/')
                    return -INF / (int(number[5]) - '0');
            }
            else
            {
                if(op == '+')
                    return INF + (int(number[4]) - '0');
                else if(op == '-')
                    return INF - (int(number[4]) - '0');
                else if(op == '*')
                    return INF * (int(number[4]) - '0');
                else if(op == '/')
                    return INF / (int(number[4]) - '0');
            }
        }
    }

    // Verific daca number este +/-E
    if(strstr(number, "E"))
    {
        if((strlen(number) == 1) || (strlen(number) == 2))
        {
            if(number[0] == '-')
                return -E;
            else
                return E;
        }
        else
        {
            char op;
            if(number[0] == '-')
                op = number[2];
            else
                op = number[1];

            if(number[0] == '-')
            {
                if(op == '+')
                    return -E + (int(number[3]) - '0');
                else if(op == '-')
                    return -E - (int(number[3]) - '0');
                else if(op == '*')
                    return -E * (int(number[3]) - '0');
                else if(op == '/')
                    return -E / (int(number[3]) - '0');
            }
            else
            {
                if(op == '+')
                    return E + (int(number[2]) - '0');
                else if(op == '-')
                    return E - (int(number[2]) - '0');
                else if(op == '*')
                    return E * (int(number[2]) - '0');
                else if(op == '/')
                    return E / (int(number[2]) - '0');
            }
        }
    }

    // Verific daca number este +/-PI
    if(strstr(number, "PI"))
    {
        if((strlen(number) == 2) || (strlen(number) == 3))
        {
            if(number[0] == '-')
                return -PI;
            else
                return PI;
        }
        else
        {
            char op;
            if(number[0] == '-')
                op = number[3];
            else
                op = number[2];

            if(number[0] == '-')
            {
                if(op == '+')
                    return -PI + (int(number[4]) - '0');
                else if(op == '-')
                    return -PI - (int(number[4]) - '0');
                else if(op == '*')
                    return -PI * (int(number[4]) - '0');
                else if(op == '/')
                    return -PI / (int(number[4]) - '0');
            }
            else
            {
                if(op == '+')
                    return PI + (int(number[3]) - '0');
                else if(op == '-')
                    return PI - (int(number[3]) - '0');
                else if(op == '*')
                    return PI * (int(number[3]) - '0');
                else if(op == '/')
                    return PI / (int(number[3]) - '0');
            }
        }
    }

    float x=0;
    int i, dotIndex;
    bool minusExists = false;
    bool dotExists = false;

    // Verific daca exista minus
    if(number[0] == '-')
        minusExists = true;
    else
        x = int(number[0] - int('0'));

    // Partea intreaga
    for(i=1; i<strlen(number); i++)
    {
        if(number[i] == '.')
        {
            dotExists = true;
            dotIndex = i;
            break;
        }
        else
            x = x*10 + int(number[i] - int('0'));
    }

    // Partea fractionara (daca exista)
    if(dotExists == true)
    {
        float fractX = 0;
        for(i=dotIndex+1; i<strlen(number); i++)
            fractX = fractX*10 + int(number[i] - int('0'));
        while(int(fractX) != 0)
            fractX /= 10;
        x = x + fractX;
    }

    if(minusExists == true)
        return -x;
    return x;
}

float onlyThreeDigits(float x)
{
    /*
        Pastreaza doar 3 cifre din partea fractionara a unui float.
        Exemple:
            onlyThreeDigits(7.39819231) => 7.398
            onlyThreeDigits(50) => 50
    */
    if(x == int(x))
        return x;

    // Exista parte fractionara
    char* charX = new char[31];
    charX = convertFloatToChar(x);
    int dotIndex=0;
    while(charX[dotIndex] != '.')
        dotIndex++;
    charX[dotIndex+4] = NULL;
    return convertCharToFloat(charX);
}
