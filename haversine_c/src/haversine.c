#ifndef HAVERSINE_C
#define HAVERSINE_C

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "base.h"

const f64 earth_radius = 6372.8;

typedef struct Pair {
    f64 x0;
    f64 y0;
    f64 x1;
    f64 y1;
} Pair;

Pair *alloc_pairs(i32 count) {
    Pair *pairs = malloc(count * sizeof(Pair));
    if (pairs == NULL) {
        fprintf(stderr, "Could not allocate a buffer for the JSON data\n");
        exit(EXIT_FAILURE);
    }
    return pairs;
}

f64 square(f64 v) { return v * v; }

f64 deg2rad(f64 deg) { return 0.01745329251994329577 * deg; }

f64 haversine_0(f64 x0, f64 y0, f64 x1, f64 y1, f64 radius) {
    f64 lat1 = y0;
    f64 lat2 = y1;
    f64 lon1 = x0;
    f64 lon2 = x1;

    f64 dLat = deg2rad(lat2 - lat1);
    f64 dLon = deg2rad(lon2 - lon1);
    lat1 = deg2rad(lat1);
    lat2 = deg2rad(lat2);

    f64 a = square(sin(dLat / 2.0)) + cos(lat1) * cos(lat2) * square(sin(dLon / 2));
    f64 c = 2.0 * asin(sqrt(a));

    f64 result = radius * c;

    return result;
}

f64 haversine_pair_0(Pair pair) {
    return haversine_0(pair.x0, pair.y0, pair.x1, pair.y1, earth_radius);
}

#endif
