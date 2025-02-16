#ifndef SLICE_C
#define SLICE_C

#include <stdint.h>
#include <string.h>
#include "arena.c"

typedef struct Slice {
    char* str;
    uint32_t len;
} Slice;


Slice slice_cat(Arena* arena, Slice a, Slice b) {
    uint32_t len = a.len + b.len;

    char* ptr = arena_alloc(arena, len);
    memcpy(ptr, a.str, a.len);
    memcpy(ptr + a.len, b.str, b.len);

    Slice new = { .str = ptr, .len = len };
    return new;
}


#endif
