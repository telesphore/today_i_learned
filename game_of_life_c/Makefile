CC = gcc
CFLAGS = -Wall -Wextra -std=c2x -pedantic
OPTFLAGS = -O3 -march=native -mavx -mavx2 -mfma -msse -msse2 -msse3
LIBFLAGS = -lraylib -lGL -lm -lpthread -ldl -lrt -lX11
SRC = src/main.c src/game.c
TARGET = c-out/game_of_life_c

game_of_life: $(SRC)
	$(CC) src/main.c -o $(TARGET) $(CFLAGS) $(OPTFLAGS) $(LIBFLAGS)

asm: game_of_life
	objdump -Sd $(TARGET) > junk/$(TARGET).asm

