#include <stdint.h>
#include <immintrin.h>

#include "raylib.h"

#include "game.c"

int main(void) {
    Game game = {0};
    init(&game);
    randomize(&game);

    InitWindow(SCREEN, SCREEN, "Game of Life (c)");

    // SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();

        ClearBackground(BLACK);

        draw_cells(&game);

        DrawFPS(20, 20);
        EndDrawing();
    }

    deinit(&game);
    return 0;
}
