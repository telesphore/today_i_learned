#include <ctype.h>
#include <getopt.h>
#include <setjmp.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "base.h"
#include "haversine.c"
#include "profiler.c"

typedef struct Args {
    char *json_file;
} Args;

typedef struct Json {
    char *buff;
    char *name;
    i64 len;
} Json;

const char *HELP =
    "Given a set of pairs of latitude and longitude, calculate their haversine distances."
    "calculate -j JSON\n"
    "-j FILE: The name of the JSON file with the lat/lon pairs.";

Args parse_args(int argc, char **argv) {
    Args args = {
        .json_file = NULL,
    };
    i8 opt;

    while ((opt = getopt(argc, argv, "j:")) != -1) {
        switch (opt) {
            case 'j':
                args.json_file = optarg;
                break;

            case '?':
                fprintf(stderr, "%s\n", HELP);
        }
    }

    if (args.json_file == NULL) {
        fprintf(stderr, "-j FILE is required\n");
        exit(EXIT_FAILURE);
    }

    return args;
}

void read_file(FILE *file, Json *json) {
    block_bandwidth("fread json", json->len);
    i64 read = fread(json->buff, 1, json->len, file);
    if (read != json->len) {
        fprintf(stderr, "Could not read %s\n", json->name);
        exit(EXIT_FAILURE);
    }
    block_end();
}

Json read_json(char *file_name) {
    Json json = {.name = file_name};

    FILE *file = fopen(file_name, "r");
    if (file == NULL) {
        fprintf(stderr, "Failed to open JSON file %s\n", file_name);
        exit(EXIT_FAILURE);
    }

    if (fseek(file, 0L, SEEK_END) == -1) {
        fprintf(stderr, "Could not seek %s\n", file_name);
        exit(EXIT_FAILURE);
    }

    json.len = ftell(file);
    if (json.len == -1) {
        fprintf(stderr, "Could not tell %s\n", json.name);
        exit(EXIT_FAILURE);
    }

    if (fseek(file, 0L, 0) == -1) {
        fprintf(stderr, "Could not seek %s\n", file_name);
        exit(EXIT_FAILURE);
    }

    block_start("alloc json");
    json.buff = malloc(json.len + 1);
    if (json.buff == NULL) {
        fprintf(stderr, "Could not allocate a buffer for the JSON data\n");
        exit(EXIT_FAILURE);
    }
    block_end();

    read_file(file, &json);

    fclose(file);

    json.buff[json.len] = 0; // Null terminate string

    return json;
}

inline char *skip_ws(char *json) {
    while (json[0] && isspace(json[0])) {
        ++json;
    }
    return json;
}

char *end_of_string(char *json) {
    while (json[0] && json[0] != '"' && json[-1] != '\\') {
        json++;
    }
    return json;
}

i32 get_count(char *json) {
    char *end;
    json = strstr(json, "\"count\"") + 7; // Skip label "count"
    json = skip_ws(json) + 1;             // Skip colon :
    json = skip_ws(json);
    return strtol(json, &end, 10);
}

f64 get_sum(char *json) {
    char *end;
    json = strstr(json, "\"sum\"") + 5; // Skip label "count"
    json = skip_ws(json) + 1;           // Skip colon :
    json = skip_ws(json);
    return strtof(json, &end);
}

void parse_json_pairs(char *json, Pair *pairs, i32 count) {
    char *end;

    // Pairs start off like: "pairs": [
    json = strstr(json, "\"pairs\"") + 7; // Skip label "pairs"
    json = skip_ws(json) + 1;             // Skip colon :
    json = skip_ws(json) + 1;             // Skip open square backet [

    // Each pair looks similar to this:
    //      {"x0":   18.6669, "y0": -84.7273, "x1":  -98.5849, "y1":  -8.1894},
    for (i32 i = 0; i < count; ++i) {
        json = skip_ws(json) + 1; // Skip open curly bracket {

        for (i32 j = 0; j < 4; ++j) {
            json = skip_ws(json) + 1; // Skip open quote "

            char *prev = json;              // Save the key location
            json = end_of_string(json) + 1; // Skip closing quote
            json = skip_ws(json) + 1;       // Skip colon

            f64 value = strtod(json, &end);
            if (prev[0] == 'x' && prev[1] == '0') {
                pairs[i].x0 = value;
            } else if (prev[0] == 'y' && prev[1] == '0') {
                pairs[i].y0 = value;
            } else if (prev[0] == 'x' && prev[1] == '1') {
                pairs[i].x1 = value;
            } else if (prev[0] == 'y' && prev[1] == '1') {
                pairs[i].y1 = value;
            }

            json = end; // Get passed the parsed value
            json = skip_ws(json);

            json = json[0] == ',' ? json + 1 : json;
            json = skip_ws(json);
        }

        json = skip_ws(json) + 1; // Skip passed closing curly backet
        json = skip_ws(json) + 1; // Skip passed comma separator
    }
}

int main(int argc, char **argv) {
    start_profiler();

    block_start("parse args");
    Args args = parse_args(argc, argv);
    block_end();

    block_start("read json");
    Json json = read_json(args.json_file);
    block_end();

    block_start("get count");
    i32 count = get_count(json.buff);
    block_end();

    block_start("get sum");
    f64 ori_sum = get_sum(json.buff);
    block_end();

    block_bandwidth("alloc pairs", json.len);
    Pair *pairs = alloc_pairs(count);
    block_end();

    block_bandwidth("parse pairs", json.len);
    parse_json_pairs(json.buff, pairs, count);
    block_end();

    block_bandwidth("calc", count * sizeof(Pair));
    f64 sum = 0.0;
    for (i32 i = 0; i < count; ++i) {
        block_bandwidth("calc one", sizeof(Pair));
        Pair p = pairs[i];
        sum += haversine_pair_0(p);
        block_end();
    }
    sum /= (f64)count;
    block_end();

    printf("\noriginal %8.4f - %8.4f = %8.4f\n\n", ori_sum, sum, ori_sum - sum);

    block_start("free");
    free(json.buff);
    block_end();

    end_profiler();

    return 0;
}
