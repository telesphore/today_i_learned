#include <stdint.h>

#include "base.h"
#include "profiler.c"

int main(void) {
    start_profiler();
    u64 os_freq = get_os_timer_freq();

    block_start("First block");
    u64 os_start = read_os_timer();
    u64 os_end = 0;
    u64 os_elapsed = 0;

    while (os_elapsed < os_freq) {
        os_end = read_os_timer();
        os_elapsed = os_end - os_start;
    }

    block_end();

    end_profiler();

    return 0;
}
