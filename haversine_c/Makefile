.PHONY: clean

CC = gcc-12
CFLAGS = -Wall -Wextra -std=c2x -pedantic
OPTFLAGS = -O3 -march=native -mavx -mavx2 -mfma -msse -msse2 -msse3
LIBFLAGS = -lm
DEPS = src/generate.c src/haversine.c src/profiler.c src/base.h

all: bin/generate bin/calculate bin/timeit

bin/generate: $(DEPS) src/generate.c
	$(CC) src/generate.c -o bin/generate $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

bin/calculate: $(DEPS) src/calculate.c
	$(CC) src/calculate.c -o bin/calculate $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

bin/timeit: $(DEPS) src/timeit.c
	$(CC) src/timeit.c -o bin/timeit $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

clean:
	rm bin/*

