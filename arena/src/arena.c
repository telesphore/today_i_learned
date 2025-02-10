#ifndef ARENA_C
#define ARENA_C

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define ARENA_ALIGN (2 * sizeof(void*))

typedef struct Arena {
    unsigned char* start;
    unsigned char* next;
    unsigned char* end;
} Arena;

Arena* arena_init(Arena* arena, void* buffer, size_t capacity) {
    arena->start = buffer;
    arena->next = 0;
    arena->end = (unsigned char*)buffer + capacity;
    return arena;
}

bool is_power_of_2(uintptr_t x) {
    return (x & (x - 1)) == 0;
}

unsigned char* arena_align(unsigned char* ptr, size_t align) {
    assert(is_power_of_2(align));

    uintptr_t modulo = (uintptr_t)ptr & (align - 1);
    ptr += modulo == 0 ? 0 : align - modulo;
    return ptr;
}

void* arena_alloc_align(Arena* arena, size_t size, size_t align) {
    unsigned char* curr = arena_align(arena->next, align);

    if (curr >= arena->end) { return NULL; }

    arena->next = curr + size;

    memset(curr, 0, size);

    return curr;
}

void* arena_alloc(Arena* arena, size_t size) {
    return arena_alloc_align(arena, size, ARENA_ALIGN);
}

void arena_free_all(Arena* arena) {
    arena->next = 0;
}

#endif
