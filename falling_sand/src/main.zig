const std = @import("std");

const ray = @cImport({
    @cInclude("raylib.h");
});

const print = std.debug.print;

const CELL: c_int = 4;
const COUNT: c_int = 300;
const COUNT_M1 = COUNT - 1;
const SCREEN: c_int = COUNT * CELL;

const COLOR: [17]ray.struct_Color = .{
    ray.YELLOW,
    ray.GOLD,
    ray.ORANGE,
    ray.PINK,
    ray.RED,
    ray.MAGENTA,
    ray.MAROON,
    ray.LIME,
    ray.GREEN,
    ray.DARKGREEN,
    ray.SKYBLUE,
    ray.BLUE,
    ray.DARKBLUE,
    ray.VIOLET,
    ray.PURPLE,
    ray.DARKPURPLE,
    //
    // ray.BLACK,
    // ray.BEIGE,
    // ray.BROWN,
    // ray.DARKBROWN,
    // ray.Color{ .r = 0, .g = 255, .b = 255, .a = 255 }, // CYAN
    ray.Color{ .r = 32, .g = 32, .b = 32, .a = 255 }, // darker gray
    // ray.LIGHTGRAY,
    // ray.GRAY,
    // ray.DARKGRAY,
    // ray.WHITE,
};

const EMPTY: u8 = 16;

const Grid = struct {
    allocator: std.mem.Allocator,
    curr: []u8,
    prev: []u8,
    color_idx: u8 = 2,
    grains: u32 = 0,

    fn init(allocator: std.mem.Allocator) !Grid {
        const curr = try allocator.alloc(u8, COUNT * COUNT);
        errdefer allocator.free(curr);

        const prev = try allocator.alloc(u8, COUNT * COUNT);
        errdefer allocator.free(prev);

        @memset(curr, EMPTY);
        @memset(prev, EMPTY);

        return .{
            .curr = curr,
            .prev = prev,
            .allocator = allocator,
        };
    }

    fn deinit(self: Grid) void {
        self.allocator.free(self.prev);
        self.allocator.free(self.curr);
    }

    fn update_cells(self: *Grid) void {
        self.swap_buffers();

        var prng = std.Random.DefaultPrng.init(99706354);
        const rand = prng.random();

        @memset(self.curr, EMPTY);

        for (0..COUNT) |row| {
            for (0..COUNT) |col| {
                const cell_idx = index(row, col);
                const color = self.prev[cell_idx];

                if (color == EMPTY) continue;

                const can_down = row < COUNT_M1;
                const can_left = col > 0;
                const can_right = col < COUNT_M1;
                const left_first = rand.uintLessThan(u8, 2) == 0;

                if (can_down and self.is_empty(row + 1, col)) {
                    self.curr[index(row + 1, col)] = color;
                } else if (left_first and can_down and can_left and self.is_empty(row + 1, col - 1)) {
                    self.curr[index(row + 1, col - 1)] = color;
                } else if (can_down and can_right and self.is_empty(row + 1, col + 1)) {
                    self.curr[index(row + 1, col + 1)] = color;
                } else if (can_down and can_left and self.is_empty(row + 1, col - 1)) {
                    self.curr[index(row + 1, col - 1)] = color;
                } else {
                    self.curr[cell_idx] = color;
                }
            }
        }
    }

    fn is_empty(self: Grid, row: usize, col: usize) bool {
        return self.prev[index(row, col)] == EMPTY;
    }

    fn draw_cells(self: Grid) void {
        for (0..COUNT) |row| {
            const r: c_int = @intCast(row);
            for (0..COUNT) |col| {
                const c: c_int = @intCast(col);
                ray.DrawRectangle(c * CELL, r * CELL, CELL, CELL, COLOR[self.curr[index(row, col)]]);
            }
        }
    }

    fn swap_buffers(self: *Grid) void {
        // self.curr ^= self.prev;
        // self.prev ^= self.curr;
        // self.curr ^= self.prev;
        const tmp = self.prev;
        self.prev = self.curr;
        self.curr = tmp;
    }

    fn cell_color(self: *Grid) u8 {
        self.grains += 1;
        if (self.grains & 0x0000007F == 0) {
            self.color_idx += 1;
            self.color_idx &= 0x0F;
        }
        return self.color_idx;
    }

    fn index(row: usize, col: usize) usize {
        return row * COUNT + col;
    }
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    ray.InitWindow(SCREEN, SCREEN, "Falling Sand (zig)");
    defer ray.CloseWindow();

    var grid = try Grid.init(allocator);
    defer grid.deinit();

    // ray.SetTargetFPS(120);

    while (!ray.WindowShouldClose()) {
        if (ray.IsMouseButtonDown(ray.MOUSE_BUTTON_LEFT)) {
            const pos = ray.GetMousePosition();
            if (pos.x >= 0 and pos.x < SCREEN and pos.y >= 0 and pos.y < SCREEN) {
                const row: usize = @intFromFloat(@floor(pos.y / CELL));
                const col: usize = @intFromFloat(@floor(pos.x / CELL));
                const idx = Grid.index(row, col);
                if (grid.curr[idx] == EMPTY) grid.curr[idx] = grid.cell_color();
            }
        }
        {
            ray.BeginDrawing();
            defer ray.EndDrawing();

            grid.draw_cells();

            ray.DrawFPS(10, 10);
        }

        grid.update_cells();
    }
}
