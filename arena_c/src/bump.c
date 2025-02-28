#ifndef BUMP_C
#define BUMP_C

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define BUMP_ALIGN (2 * sizeof(void*))

typedef struct Bump {
    unsigned char* buff;
    size_t next;
    size_t end;
} Bump;

Bump* bump_init(Bump* bump, void* buffer, size_t capacity) {
    bump->buff = buffer;
    bump->next = 0;
    bump->end = capacity;
    return bump;
}

bool is_power_of_2(uintptr_t x) {
    return (x & (x - 1)) == 0;
}

uintptr_t bump_align(uintptr_t ptr, size_t align) {
    assert(is_power_of_2(align));

    uintptr_t modulo = ptr & (align - 1);
    ptr += modulo == 0 ? 0 : align - modulo;
    return ptr;
}

void* bump_alloc_align(Bump* bump, size_t size, size_t align) {
    uintptr_t next = bump_align(bump->next, align);

    if (next >= bump->end) { return NULL; }

    bump->next = next + size;

    void* ptr = &bump->buff[next];
    memset(ptr, 0, size);

    return ptr;
}

void* bump_alloc(Bump* bump, size_t size) {
    return bump_alloc_align(bump, size, BUMP_ALIGN);
}

void bump_free_all(Bump* bump) {
    bump->next = 0;
}

#endif
