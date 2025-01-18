const std = @import("std");

const ray = @cImport({
    @cInclude("raylib.h");
});

const g = @import("game.zig");

pub fn main() !void {
    ray.InitWindow(g.SCREEN, g.SCREEN, "Game of Life (zig)");
    defer ray.CloseWindow();

    var prng = std.Random.DefaultPrng.init(99706354);
    const rand = prng.random();

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var game = try g.Game.init(allocator, rand);
    defer game.deinit();

    game.randomize();

    // ray.SetTargetFPS(10);

    while (!ray.WindowShouldClose()) {
        ray.BeginDrawing();
        defer ray.EndDrawing();

        ray.ClearBackground(ray.BLACK);

        game.draw_cells();

        ray.DrawFPS(10, 10);
    }
}
