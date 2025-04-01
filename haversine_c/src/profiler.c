#ifndef PROFILER_C
#define PROFILER_C

#define PROFILE 1

#include <stdio.h>
#include <sys/time.h>
#include <x86intrin.h>

#include "base.h"

typedef struct ProfilerBlock {
    u64 start;
    u64 end;
    u64 elapsed;
    u64 children;
    u64 bytes;
    char *label;
    u32 hits;
} ProfilerBlock;

#define MAX_BLOCKS 256

ProfilerBlock BLOCKS[MAX_BLOCKS] = {0};

u32 PROFILER_STACK[1024] = {0};
i32 PROFILER_STACK_IDX = -1;

f64 MEGABYTE = 1024.0 * 1024.0;
f64 GIGABYTE = 1024.0 * 1024.0 * 1024.0;

static u64 get_os_timer_freq(void) {
    return 1000000;
}

static u64 read_os_timer(void) {
    struct timeval value;
    gettimeofday(&value, 0);

    u64 result = get_os_timer_freq() * (u64)value.tv_sec + (u64)value.tv_usec;
    return result;
}

inline u64 read_cpu_timer(void) {
    return __rdtsc();
}

static u64 estimate_cpu_timer_freq(void) {
    u64 msec_to_wait = 100;
    u64 os_freq = get_os_timer_freq();

    u64 cpu_start = read_cpu_timer();
    u64 os_start = read_os_timer();
    u64 os_end = 0;
    u64 os_elapsed = 0;
    u64 os_wait_time = os_freq * msec_to_wait / 1000;

    while (os_elapsed < os_wait_time) {
        os_end = read_os_timer();
        os_elapsed = os_end - os_start;
    }

    u64 cpu_end = read_cpu_timer();
    u64 cpu_elapsed = cpu_end - cpu_start;

    u64 cpu_freq = 0;
    if (os_elapsed) {
        cpu_freq = os_freq * cpu_elapsed / os_elapsed;
    }

    return cpu_freq;
}

void block_start_idx(i32 idx, char *label, u64 bytes) {
    ++PROFILER_STACK_IDX;
    PROFILER_STACK[PROFILER_STACK_IDX] = idx;
    BLOCKS[idx].start = read_cpu_timer();
    BLOCKS[idx].label = label;
    BLOCKS[idx].bytes += bytes;
    ++BLOCKS[idx].hits;
}

#if PROFILE != 0
#define block_start(label) block_start_idx(__COUNTER__ + 1, label, 0)
#define block_bandwidth(label, bytes) block_start_idx(__COUNTER__ + 1, label, (bytes))
#else
#define block_start(...)
#define block_bandwidth(...)
#endif

u64 get_block_elapsed(i32 idx) {
    BLOCKS[idx].end = read_cpu_timer();
    u64 elapsed = BLOCKS[idx].end - BLOCKS[idx].start;
    BLOCKS[idx].elapsed += elapsed;
    return elapsed;
}

void block_end() {
#if PROFILE != 0
    i32 idx = PROFILER_STACK[PROFILER_STACK_IDX];

    // Update current timer
    u64 elapsed = get_block_elapsed(idx);

    --PROFILER_STACK_IDX;

    // Update parent timer
    idx = PROFILER_STACK[PROFILER_STACK_IDX];
    BLOCKS[idx].children += elapsed;
#endif
}

void start_profiler(void) {
    block_start_idx(0, "Total time", 0);
}

void print_elapsed(i32 idx, u64 total_elapsed, u64 cpu_freq) {
    ProfilerBlock block = BLOCKS[idx];
    u64 children = idx ? block.children : 0;
    u64 elapsed = block.elapsed - children;
    f64 percent = 100.0 * ((f64)elapsed / (f64)total_elapsed);
    f64 ms = 1000.0 * (f64)elapsed / (f64)cpu_freq;
    printf("%-16s [%d]: %0.4f ms (%6.2f%%)", block.label, block.hits, ms, percent);
    if (block.bytes) {
        f64 sec = (f64)block.elapsed / (f64)cpu_freq;
        f64 bytes_per_sec = block.bytes / sec;
        f64 megabytes = (f64)block.bytes / MEGABYTE;
        f64 gbytes_per_sec = bytes_per_sec / GIGABYTE;

        printf("  %0.3f mb at %0.2f gb/s", megabytes, gbytes_per_sec);
    }
    printf("\n");
}

void end_profiler() {
    u64 total_elapsed = get_block_elapsed(0);
    u64 cpu_freq = estimate_cpu_timer_freq();

    for (i32 i = 0; i < MAX_BLOCKS; ++i) {
        if (!BLOCKS[i].hits) {
            break;
        }
        print_elapsed(i, total_elapsed, cpu_freq);
    }
}

#endif
