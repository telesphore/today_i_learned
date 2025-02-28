CC = gcc-12
CFLAGS = -Wall -Wextra -std=c2x -pedantic
OPTFLAGS = -O3 -march=native
LIBFLAGS =
SRC = src/main.c src/slice.c
TARGET = bin/slice

game_of_life: $(SRC)
	$(CC) src/main.c -o $(TARGET) $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

asm: slice
	objdump -Sd $(TARGET) > junk/$(TARGET).asm

