.PHONY: clean

CC = gcc-12
CFLAGS = -Wall -Wextra -std=c2x -pedantic
OPTFLAGS = -O3 -march=native -mavx -mavx2 -mfma -msse -msse2 -msse3
LIBFLAGS =

all: bin/generate bin/calculate

bin/generate: src/generate.c 
	$(CC) src/generate.c -o bin/generate $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

bin/calculate: src/calculate.c
	$(CC) src/calculate.c -o bin/calculate $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

clean:
	rm -f bin/*

