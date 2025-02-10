#ifndef GAME_C
#define GAME_C

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "raylib.h"

const int N = 256;
const int M = N - 1;

const int CELL = 4;
const int SCREEN = N * CELL;

const uint8_t ALIVE = 1;
const uint8_t DEAD = 0;

typedef struct Game {
    uint8_t *curr;
    uint8_t *old;
} Game;

void init(Game *game) {
    game->curr = (uint8_t*)calloc(N * N, sizeof(uint8_t));
    game->old =(uint8_t*)calloc(N * N, sizeof(uint8_t));
    if (!game->curr || !game->old) {
        fprintf(stderr, "Out of memory");
        exit(0);
    }
}

void deinit(Game *game) {
    free(game->old);
    free(game->curr);
}

int idx(int row, int col) {
    return row * N + col;
}

void swap_buffers(Game *game) {
    uint8_t *temp = game->curr;
    game->curr = game->old;
    game->old = temp;
}

void randomize(Game *game) {
    srand(99706354);
    for (int r = 0; r < N; ++r) {
        for (int c = 0; c < N; ++c) {
            game->curr[idx(r, c)] = (uint8_t)rand() & ALIVE;
        }
    }
}

void draw_cell(int row, int col) {
    DrawRectangle(col * CELL, row * CELL, CELL, CELL, RED);
}

uint8_t update_cell(Game *game, int row, int col) {
    const int n = row > 0 ? row - 1 : M;
    const int s = row < M ? row + 1 : 0;
    const int w = col > 0 ? col - 1 : M;
    const int e = col < M ? col + 1 : 0;

    uint8_t sum = 0;

    sum += game->old[idx(n, w)];
    sum += game->old[idx(n, col)];
    sum += game->old[idx(n, e)];

    sum += game->old[idx(row, w)];
    sum += game->old[idx(row, e)];

    sum += game->old[idx(s, w)];
    sum += game->old[idx(s, col)];
    sum += game->old[idx(s, e)];

    const uint8_t old = game->old[idx(row, col)];
    const uint8_t curr = (old == ALIVE && sum == 2) || sum == 3;

    return curr;
}

void draw_cells(Game *game) {
    swap_buffers(game);
    for (int r = 0; r < N; ++r) {
        for (int c = 0; c < N; ++c) {
            uint8_t cell = update_cell(game, r, c);
            game->curr[idx(r, c)] = cell;
            if (cell == ALIVE) {
                draw_cell(r, c);
            }
        }
    }
}

#endif
