#include <getopt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "abbrev.h"

typedef struct Args {
    u32 count;
    f64 lat_lo;
    f64 lat_hi;
    f64 lon_lo;
    f64 lon_hi;
    bool error;
} Args;

Args parse_args(int argc, char **argv) {
    Args args = {
        .lat_lo = -90.0,
        .lat_hi = 90.0,
        .lon_lo = -180.0,
        .lon_hi = 180.0,
        .error = false,
    };
    i8 opt;
    char *end;

    while ((opt = getopt(argc, argv, "c:a:A:o:O:")) != -1) {
        switch (opt) {
            case 'c':
                args.count = strtoul(optarg, &end, 10);
                if (optarg == end || *end != '\0') {
                    printf("-c count is not an integer > 0 '%s'\n", optarg);
                    args.error = true;
                }
                break;

            case 'a':
                args.lat_lo = strtof(optarg, &end);
                if (optarg == end || *end != '\0') {
                    printf("-a lat low is not a float '%s'\n", optarg);
                    args.error = true;
                }
                break;

            case 'A':
                args.lat_hi = strtof(optarg, &end);
                if (optarg == end || *end != '\0') {
                    printf("-A lat high is not a float '%s'\n", optarg);
                    args.error = true;
                }
                break;

            case 'o':
                args.lon_lo = strtof(optarg, &end);
                if (optarg == end || *end != '\0') {
                    printf("-o lon low is not a float '%s'\n", optarg);
                    args.error = true;
                }
                break;

            case 'O':
                args.lon_hi = strtof(optarg, &end);
                if (optarg == end || *end != '\0') {
                    printf("-O lon high is not a float '%s'\n", optarg);
                    args.error = true;
                }
                break;
        }
    }
    return args;
}

int main(int argc, char **argv) {
    Args args = parse_args(argc, argv);
    if (args.error) {
        return 1;
    }

    printf("%d %f %f %f %f %d\n", args.count, args.lat_lo, args.lat_hi, args.lon_lo, args.lon_hi, args.error);

    return 0;
}
