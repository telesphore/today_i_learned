const std = @import("std");

const ray = @cImport({
    @cInclude("raylib.h");
});

const print = std.debug.print;

const CELL: c_int = 4;

const COL_COUNT: c_int = 256;
const ROW_COUNT: c_int = 256;
const ROW_COUNT_M1 = ROW_COUNT - 1;
const COL_COUNT_M1 = COL_COUNT - 1;

const PADDED_ROWS = 1 + ROW_COUNT + 1;

const COLOR: [17]ray.struct_Color = .{
    ray.RED,
    ray.MAGENTA,
    ray.MAROON,
    ray.PINK,
    ray.ORANGE,
    ray.YELLOW,
    ray.GOLD,
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
    ray.Color{ .r = 32, .g = 32, .b = 32, .a = 255 }, // darker gray
};

const EMPTY: u8 = 16;

const Grid = struct {
    allocator: std.mem.Allocator,
    rand: std.Random,
    next: []u8,
    prev: []u8,
    color_idx: u8 = 0,
    grains: u32 = 0,

    fn init(allocator: std.mem.Allocator, rand: std.Random) !Grid {
        const next = try allocator.alloc(u8, PADDED_ROWS * COL_COUNT);
        errdefer allocator.free(next);

        const prev = try allocator.alloc(u8, PADDED_ROWS * COL_COUNT);
        errdefer allocator.free(prev);

        @memset(next, EMPTY);
        @memset(prev, EMPTY);

        return .{
            .next = next,
            .prev = prev,
            .allocator = allocator,
            .rand = rand,
        };
    }

    fn deinit(self: Grid) void {
        self.allocator.free(self.prev);
        self.allocator.free(self.next);
    }

    fn update(self: *Grid) void {
        self.swap_buffers();

        @memset(self.next, EMPTY);

        for (1..PADDED_ROWS) |row| {
            for (0..COL_COUNT) |col| {
                self.set_cell(row, col);
            }
        }
    }

    // This version is trying to convert all jmp/branch instructions into cmov instructions
    // in preperation for a kernel.
    fn set_cell2(self: *Grid, row: usize, col: usize) void {
        var idx = index(row, col);
        const color = self.prev[idx];

        const down_ok = row < ROW_COUNT;
        const left_ok = col > 0;
        const right_ok = col < COL_COUNT_M1;

        const down = index(row + 1, col);
        const down_left = index(row + 1, col - 1);
        const down_right = index(row + 1, col + 1);

        const can_down = down_ok and self.prev[down] == EMPTY;
        const can_down_left = down_ok and left_ok and self.prev[down_left] == EMPTY;
        const can_down_right = down_ok and right_ok and self.prev[down_right] == EMPTY;

        const left_overwrites = self.rand.boolean();

        idx = if (can_down_left) down_left else idx;
        idx = if (can_down_right) down_right else idx;
        idx = if (left_overwrites and can_down_left) down_left else idx;
        idx = if (can_down) down else idx;

        self.next[idx] = if (color != EMPTY) color else self.next[idx];
    }

    // The original working version
    fn set_cell(self: *Grid, row: usize, col: usize) void {
        const idx = index(row, col);
        const color = self.prev[idx];

        if (color == EMPTY) return;

        const down_ok = row < ROW_COUNT;
        const left_ok = col > 0;
        const right_ok = col < COL_COUNT_M1;

        const down = index(row + 1, col);
        const down_left = index(row + 1, col - 1);
        const down_right = index(row + 1, col + 1);

        const can_down = down_ok and self.prev[down] == EMPTY;
        const can_down_left = down_ok and left_ok and self.prev[down_left] == EMPTY;
        const can_down_right = down_ok and right_ok and self.prev[down_right] == EMPTY;

        const left_first = self.rand.boolean();

        if (can_down) {
            self.next[down] = color;
        } else if (left_first and can_down_left) {
            self.next[down_left] = color;
        } else if (can_down_right) {
            self.next[down_right] = color;
        } else if (can_down_left) {
            self.next[down_left] = color;
        } else {
            self.next[idx] = color;
        }
    }

    fn draw_cells(self: Grid) void {
        for (0..ROW_COUNT) |row| {
            const r: c_int = @intCast(row);
            for (0..COL_COUNT) |col| {
                const c: c_int = @intCast(col);
                ray.DrawRectangle(
                    c * CELL,
                    r * CELL,
                    CELL,
                    CELL,
                    COLOR[self.next[index(row, col)]],
                );
            }
        }
    }

    fn swap_buffers(self: *Grid) void {
        // self.next ^= self.prev;
        // self.prev ^= self.next;
        // self.next ^= self.prev;
        const tmp = self.prev;
        self.prev = self.next;
        self.next = tmp;
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
        return row * COL_COUNT + col;
    }
};

pub fn main() !void {
    const width: c_int = COL_COUNT * CELL;
    const height: c_int = ROW_COUNT * CELL;
    ray.InitWindow(width, height, "Falling Sand (zig)");
    defer ray.CloseWindow();

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var prng = std.Random.DefaultPrng.init(9972316);
    const rand = prng.random();

    var grid = try Grid.init(allocator, rand);
    defer grid.deinit();

    while (!ray.WindowShouldClose()) {
        grid.update();
        if (ray.IsMouseButtonDown(ray.MOUSE_BUTTON_LEFT)) {
            const pos = ray.GetMousePosition();
            if (pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height) {
                const row: usize = @intFromFloat(@floor(pos.y / CELL));
                const col: usize = @intFromFloat(@floor(pos.x / CELL));
                const idx = Grid.index(row + 1, col);
                if (grid.next[idx] == EMPTY) grid.next[idx] = grid.cell_color();
            }
        }
        {
            ray.BeginDrawing();
            defer ray.EndDrawing();

            grid.draw_cells();

            ray.DrawFPS(10, 10);
        }
    }
}
