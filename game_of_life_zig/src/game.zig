const std = @import("std");

const ray = @cImport({
    @cInclude("raylib.h");
});

pub const N: usize = 256;
pub const M: usize = N - 1;

pub const CELL: c_int = 4;
pub const SCREEN: c_int = N * CELL;

pub const ALIVE: u8 = 1;
pub const DEAD: u8 = 0;

pub const Game = struct {
    allocator: std.mem.Allocator,
    rand: std.Random,
    curr: []u8,
    old: []u8,

    pub fn init(allocator: std.mem.Allocator, rand: std.Random) !Game {
        const curr = try allocator.alloc(u8, N * N);
        errdefer allocator.free(curr);

        const old = try allocator.alloc(u8, N * N);
        errdefer allocator.free(old);

        return .{
            .curr = curr,
            .old = old,
            .allocator = allocator,
            .rand = rand,
        };
    }

    pub fn deinit(self: Game) void {
        self.allocator.free(self.old);
        self.allocator.free(self.curr);
    }

    pub fn randomize(self: *Game) void {
        for (0..N) |row| {
            for (0..N) |col| {
                self.curr[index(row, col)] = self.rand.uintLessThan(u8, 2);
            }
        }
    }

    pub fn draw_cells(self: *Game) void {
        self.swap_buffers();

        for (0..N) |row| {
            for (0..N) |col| {
                const cell = self.update_cell(row, col);
                self.curr[index(row, col)] = cell;
                if (cell == ALIVE) {
                    draw_cell(row, col);
                }
            }
        }
    }

    fn update_cell(self: Game, row: usize, col: usize) u8 {
        const n: usize = if (row > 0) row - 1 else M;
        const s: usize = if (row < M) row + 1 else 0;
        const w: usize = if (col > 0) col - 1 else M;
        const e: usize = if (col < M) col + 1 else 0;

        var sum: u8 = 0;

        sum += self.old[index(n, w)];
        sum += self.old[index(n, col)];
        sum += self.old[index(n, e)];

        sum += self.old[index(row, w)];
        sum += self.old[index(row, e)];

        sum += self.old[index(s, w)];
        sum += self.old[index(s, col)];
        sum += self.old[index(s, e)];

        const old = self.old[index(row, col)];
        const curr: u8 = @intFromBool((old == ALIVE and sum == 2) or sum == 3);

        return curr;
    }

    fn draw_cell(row: usize, col: usize) void {
        const r: c_int = @intCast(row);
        const c: c_int = @intCast(col);
        ray.DrawRectangle(
            c * CELL,
            r * CELL,
            CELL,
            CELL,
            ray.GREEN,
        );
    }

    inline fn swap_buffers(self: *Game) void {
        const tmp: []u8 = self.old;
        self.old = self.curr;
        self.curr = tmp;
    }

    inline fn index(row: usize, col: usize) usize {
        return row * N + col;
    }
};
