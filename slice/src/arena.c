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
    unsigned char* buff;
    size_t next;
    size_t end;
} Arena;

Arena* arena_init(Arena* arena, void* buffer, size_t capacity) {
    arena->buff = buffer;
    arena->next = 0;
    arena->end = capacity;
    return arena;
}

bool is_power_of_2(uintptr_t x) {
    return (x & (x - 1)) == 0;
}

uintptr_t arena_align(uintptr_t ptr, size_t align) {
    assert(is_power_of_2(align));

    uintptr_t modulo = ptr & (align - 1);
    ptr += modulo == 0 ? 0 : align - modulo;
    return ptr;
}

void* arena_alloc_align(Arena* arena, size_t size, size_t align) {
    uintptr_t next = arena_align(arena->next, align);

    if (next >= arena->end) { return NULL; }

    arena->next = next + size;

    void* ptr = &arena->buff[next];
    memset(ptr, 0, size);

    return ptr;
}

void* arena_alloc(Arena* arena, size_t size) {
    return arena_alloc_align(arena, size, ARENA_ALIGN);
}

void arena_free_all(Arena* arena) {
    arena->next = 0;
}

#endif
