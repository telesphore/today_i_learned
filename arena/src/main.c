#include <stddef.h>
#include <stdint.h>

#include <stdbool.h>

#include <stdio.h>
#include <assert.h>
/*#include <string.h>*/

#include "arena.c"

int main() {
    const size_t size = 1024;
	unsigned char buff[size];

	Arena arena = {0};
	arena_init(&arena, buff, size);

	for (int i = 0; i < 10; ++i) {
        int* j = (int*)arena_alloc(&arena, sizeof(int));
        *j = i;
		printf("%p: %d\n", (void*)j, *j);
	}

	arena_free_all(&arena);

	return 0;
}

