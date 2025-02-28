#ifndef HAVERSINE_C
#define HAVERSINE_C

//#include <math.h>
#include "abbrev.h"

const f64 earth_radius = 6372.8;


typedef struct haversine {
    f64 lng1, lat1;
    f64 lng2, lat2;
} haversine;


f64 square(f64 x) {
    return x * x;
}


f64 deg2rad(f64 deg) {
    return 0.01745329251994329577 * deg;
}



/*static f64 startingHaversine(f64 X0, f64 Y0, f64 X1, f64 Y1, f64 EarthRadius)*/
/*{*/
/*    f64 lat1 = Y0;*/
/*    f64 lat2 = Y1;*/
/*    f64 lon1 = X0;*/
/*    f64 lon2 = X1;*/
/**/
/*    f64 dLat = deg2rad(lat2 - lat1);*/
/*    f64 dLon = deg2rad(lon2 - lon1);*/
/*    lat1 = deg2rad(lat1);*/
/*    lat2 = deg2rad(lat2);*/
/**/
/*    f64 a = square(sin(dLat/2.0)) + cos(lat1)*cos(lat2)*square(sin(dLon/2));*/
/*    f64 c = 2.0*asin(sqrt(a));*/
/**/
/*    f64 Result = earth_radius * c;*/
/**/
/*    return Result;*/
/*}*/


#endif
