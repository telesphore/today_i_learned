#include <stddef.h>
#include <stdint.h>

#include <stdbool.h>

#include <stdio.h>
#include <assert.h>
/*#include <string.h>*/

#include "bump.c"
#include "unit_test.h"

int tests_run = 0;

static char* test1() {
    const size_t size = 1024;
    unsigned char buff[size];
    Bump bump = {0};
    bump_init(&bump, buff, size);
    ASSERT("Bump length", bump.end == size);
    return 0;
}


static char* all_tests() {
    TEST(test1);
    return 0;
}

int main() {
    char* result = all_tests();
    if (result != 0) {
        printf("%s\n", result);
    } else {
        printf("All tests passed\n");
    }

    return result != 0;
}

