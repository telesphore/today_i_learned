#include <getopt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "base.h"
#include "haversine.c"

typedef struct Args {
    f64 y;
    f64 Y;
    f64 x;
    f64 X;
    u32 count;
    u32 seed;
    bool error;
} Args;

const char *HELP =
    "Generate pairs of longitude (x) and latitude (y) used to calculate haversine distances between them.\n"
    "generate -c N [-a LAT] [-A LAT] [-o LON] [-O LON] [-s SEED]\n"
    "    -c COUNT: How many LAT LON pairs to generate (required)\n"
    "    [-x LON]: Minimum longitude (default -180.0)\n"
    "    [-X LON]: Maximum longitude (default  180.0)\n"
    "    [-y LAT]: Minimum latitude (default -90.0)\n"
    "    [-Y LAT]: Maximum latitude (default  90.0)\n"
    "    [-s SEED]: Random number generator seed (default 3390266)";

void fatal(char *msg) {
    printf("%s\n", msg);
    exit(1);
}

Args parse_args(int argc, char **argv) {
    Args args = {
        .seed = 3390266,
        .count = 0,
        .y = -90.0,
        .Y = 90.0,
        .x = -180.0,
        .X = 180.0,
    };
    i8 opt;
    char *end;

    while ((opt = getopt(argc, argv, "c:y:Y:x:X:s:")) != -1) {
        switch (opt) {
            case 'c':
                args.count = strtoul(optarg, &end, 10);
                if (optarg == end || *end != '\0' || args.count < 1) {
                    fprintf(stderr, "-c count is not an integer > 0 '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'y':
                args.y = strtof(optarg, &end);
                if (optarg == end || *end != '\0' || args.y < -90.0 || args.y > 90.0) {
                    fprintf(stderr, "-y lat low is not valid latitude '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'Y':
                args.Y = strtof(optarg, &end);
                if (optarg == end || *end != '\0' || args.Y < -90.0 || args.Y > 90.0) {
                    fprintf(stderr, "-Y lat high is not valid latitude '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'x':
                args.x = strtof(optarg, &end);
                if (optarg == end || *end != '\0' || args.x < -180.0 || args.x > 180.0) {
                    fprintf(stderr, "-x lon low is not valid longitude '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'X':
                args.X = strtof(optarg, &end);
                if (optarg == end || *end != '\0' || args.X < -180.0 || args.X > 180.0) {
                    fprintf(stderr, "-X lon high is not a valid longitude '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case 's':
                args.seed = strtoul(optarg, &end, 10);
                if (optarg == end || *end != '\0' || args.seed < 1) {
                    fprintf(stderr, "-s seed is not an integer '%s'\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;

            case '?':
                fprintf(stderr, "%s\n", HELP);
                exit(EXIT_FAILURE);
        }
        if (args.error) {
            return args;
        }
    }

    if (args.count < 1) {
        fprintf(stderr, "-c COUNT is required\n");
        exit(EXIT_FAILURE);
    }

    if (args.y >= args.Y) {
        fprintf(stderr, "-y LAT low %f must be less than -Y LAT high %f", args.y, args.Y);
        exit(EXIT_FAILURE);
    }

    if (args.x >= args.X) {
        fprintf(stderr, "-x LON low %f must be less than -X LON high %f", args.x, args.X);
        exit(EXIT_FAILURE);
    }

    return args;
}

int main(int argc, char **argv) {
    Args args = parse_args(argc, argv);

    srand(args.seed);
    f64 y_range = args.Y - args.y;
    f64 x_range = args.X - args.x;

    Pair *pairs = alloc_pairs(args.count);
    f64 *distances = malloc(args.count * sizeof(f64));

    f64 sum = 0.0;

    for (u32 i = 0; i < args.count; ++i) {
        pairs[i].y0 = args.y + ((f64)rand() / (f64)RAND_MAX) * y_range;
        pairs[i].x0 = args.x + ((f64)rand() / (f64)RAND_MAX) * x_range;
        pairs[i].y1 = args.y + ((f64)rand() / (f64)RAND_MAX) * y_range;
        pairs[i].x1 = args.x + ((f64)rand() / (f64)RAND_MAX) * x_range;

        distances[i] = haversine_pair_0(pairs[i]);
        sum += distances[i];
    }

    sum /= (f64)args.count;

    printf("{\n");
    printf("    \"count\": %d,\n", args.count);
    printf("    \"seed\":  %d,\n", args.seed);
    printf("    \"x_min\": %11f,\n", args.x);
    printf("    \"x_max\": %11f,\n", args.X);
    printf("    \"y_min\": %11f,\n", args.y);
    printf("    \"y_max\": %11f,\n", args.Y);
    printf("    \"sum\":%24.16f,\n", sum);
    printf("    \"pairs\": [\n");

    for (u32 i = 0; i < args.count; ++i) {
        Pair p = pairs[i];
        char *comma = i == args.count - 1 ? "" : ",";
        printf(
            "        {\"x0\": %21.16f, \"y0\": %20.16f, \"x1\": %21.16f, \"y1\": %20.16f}%s\n",
            p.x0, p.y0, p.x1, p.y1, comma);
    }
    printf("    ],\n");

    printf("    \"distances\": [\n");
    for (u32 i = 0; i < args.count; ++i) {
        printf("        %24.16f,\n", distances[i]);
    }
    printf("    ]\n");

    printf("}");

    free(distances);
    free(pairs);

    return 0;
}
