#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

    struct Point;
    void setStep(float a, float b, float &step);
    void setScaleY(float &maxValueOfFunction, int nPoints, Point points[], float &signedMin, float &signedMax);
    void setScaleX(int nPoints, Point points[], float &a, float &b);

#ifdef __cplusplus
} //end extern "C"
#endif // __cplusplus
