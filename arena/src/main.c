#include <stddef.h>
#include <stdint.h>

#include <stdbool.h>

#include <stdio.h>
#include <assert.h>
/*#include <string.h>*/

#include "arena.c"
#include "unit_test.h"

int tests_run = 0;

static char* test1() {
    const size_t size = 1024;
    unsigned char buff[size];
    Arena arena = {0};
    arena_init(&arena, buff, size);
    ASSERT("Arena length", arena.end == arena.start + size);
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

    /**/
    /*   const size_t size = 1024;*/
    /*unsigned char buff[size];*/
    /**/
    /*Arena arena = {0};*/
    /*arena_init(&arena, buff, size);*/
    /**/
    /*for (int i = 0; i < 10; ++i) {*/
    /*       int* j = (int*)arena_alloc(&arena, sizeof(int));*/
    /*       *j = i;*/
    /* printf("%p: %d\n", (void*)j, *j);*/
    /*}*/
    /**/
    /*arena_free_all(&arena);*/

    return result != 0;
}

