#include <stdio.h>

#include "abbrev.h"

int main(int argc, char** argv) {
    printf("%d \n", argc);

    for (i32 i = 0; i < argc; ++i) {
        printf("%s\n", argv[i]);
    }

    return 0;
}
