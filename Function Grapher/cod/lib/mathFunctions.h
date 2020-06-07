using namespace std;

bool isRadian = true;

void setUsingRadiansTo(bool usingRadians) {
    isRadian = usingRadians;
}

double Sinus(double degrees) {
    double result;
    if (isRadian)
        result = sin(degrees); // cu radiani
    else
        result = sin(degrees*PI/180); // cu grade

    if ((result < EPSILON  && result >= 0) || (result > -EPSILON && result < 0))
        return 0.0;
    return result;
}

double Cosinus(double degrees) {
    double result;
    if (isRadian)
        result = cos(degrees);
    else
        result = cos(degrees*PI/180);

    if ((result < EPSILON  && result >= 0) || (result > -EPSILON && result < 0))
        return 0.0;
    return result;
}

double Tangent(double degrees) {
    double result;
    if (isRadian)
        result = tan(degrees);
    else
        result = tan(degrees*PI/180);

    if (result > INFINIT)
        return INFINITY;
    else if(result < -INFINIT)
        return -INFINITY;

    if ((result < EPSILON && result >= 0) || (result > -EPSILON && result < 0))
        return 0.0;

    return result;
}

double Cotangent(double degrees) {
    double result;
    result = 1/Tangent(degrees);

    return result;
}

double arcSinus(double value) {
    double result = asin(value);
    if (isRadian)
        return result;
    else
        return result*180/PI;
}

double arcCosinus(double value) {
    double result = acos(value);
    if (isRadian)
        return result;
    else
        return result*180/PI;
}

double arcTangent(double value) {
    double result = atan(value);
    if (isRadian)
        return result;
    else
        return result*180/PI;
}

double arcCotangent(double value) {
    double result = PI/2 - atan(value);
    if (isRadian)
        return result;
    else
        return result*180/PI;
}

double Radical(double Value) {
	// Radacina patrata a unui numar
    if (Value < 0)
        return NAN;
    if (Value > INFINIT)
        return INFINITY;
    return sqrt(Value);
}

double Log(double Value) {
	// Logaritm natural dintr-un numar
    if (Value < 0)
        return NAN;
    if (Value == 0)
        return -INFINITY;
    if (Value > INFINIT)
        return INFINITY;
    return log(Value);
}

double LogInBase(double Value, double Base = E) {
	// Logaritm din x in baza b;
    if (Value == 0)
        return NAN;
    return Log(Value)/Log(Base);
}

double Power(double Value1, double Value2) {
	// Ridicarea la putere(x la puterea y)
    if (Value1 == 0)
        return 0.0;
    if (Value2 == 0)
        return 1.0;

    double result = pow(Value1, Value2);

    if (result > INFINIT)
        return INFINITY;
    else if (result < -INFINIT)
        return -INFINITY;

    return result;
}

double Plus(double Value1, double Value2) {
	// Adunarea a doua numere
    if (Value1 > INFINIT || Value2 > INFINIT)
        return INFINITY;

    double result = Value1+Value2;
    if (result > INFINIT)
        return INFINITY;
    else if (result < -INFINIT)
        return -INFINITY;
    return result;
}

double Minus(double Value1, double Value2) {
	// Scaderea a doua numere
    double result = Value1-Value2;
    if (result > INFINIT)
        return INFINITY;
    else if (result < -INFINIT)
        return -INFINITY;
    return result;
}

double UnaryMinus(double Value) {
    if (Value < 0 && Value < -INFINIT)
        return INFINITY;
    else if (Value > 0 && Value > INFINIT)
        return -INFINITY;

    return -Value;
}

double UnaryPlus(double Value) {
    if (Value < 0 && Value < -INFINIT)
        return -INFINITY;
    else if (Value > 0 && Value > INFINIT)
        return INFINITY;

    return Value;
}


double Multiply(double Value1, double Value2) {
	// Inmultirea a doua numere
    if (Value1 == 0 || Value2 == 0)
        return 0.0;

    if (Value1 > INFINIT || Value2 > INFINIT)
        return INFINITY;

    double result = Value1*Value2;
    if (result > INFINIT)
        return INFINITY;
    else if (result < -INFINIT)
        return -INFINITY;
    return result;
}

double Divide(double Value1, double Value2) {
	// Impartirea a doua numere
    if (Value1 == 0 && Value2 != 0)
        return 0.0;
    if (Value2 == 0 && Value1 != 0)
        return INFINITY;
    if (Value1 == 0 && Value2 == 0)
        return NAN;

    double result = Value1/Value2;
    if (result > INFINIT)
        return INFINITY;
    else if (result < -INFINIT)
        return -INFINITY;
    else if ((result < EPSILON  && result >= 0) || (result > -EPSILON && result < 0))
        return 0.0;
    return result;
}

double Modulo(double Value1, double Value2) {
	// Restul impartirii a doua numere
    if (Value2 == 0)
        return NAN;
    if (Value1>INFINIT || Value2>INFINIT)
        return INFINITY;
    return (int)Value1 % (int)Value2;
}

double Absolute(double Value) {
	// Valoare absoluta (Modul)
    if (abs(Value) > INFINIT)
        return INFINITY;
    if (Value < 0)
        return -Value;
    return Value;
}


int Equal(double Value1, double Value2) {
	// Verifica daca sunt egale
    if (Value1==Value2)
        return 1;
    else
        return 0;
}

int notEqual(double Value1, double Value2) {
	// Verifica daca nu sunt egale
    if (Value1!=Value2)
        return 1;
    else
        return 0;
}

int Greater(double Value1, double Value2) {
	// x mai mare decat y
    if (Value1 > Value2)
        return 1;
    return 0;
}

int greaterOrEqual(double Value1, double Value2) {
	// x mai mare sau egal cu y
    if (Value1 >= Value2)
        return 1;
    return 0;
}

int Less(double Value1, double Value2) {
	// x mai mic decat y
    if (Value1 < Value2)
        return 1;
    return 0;
}

int lessOrEqual(double Value1, double Value2) {
	// x mai mic sau egal cu y
    if (Value1 <= Value2)
        return 1;
    return 0;
}




