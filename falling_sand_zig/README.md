# Falling Sand

This classic simulation shows grains of colored sand falling. Drag the mouse (left button) across the window to spawn the sand grains.

I'm using this to familiarize myself with Zig and RayLib.

### TODO: If I ever get back to this

- [ ] Add gravity: Umm.... Falling.
- [ ] Use GPU shaders: The algorithm is embarrassingly parallel.
- [ ] Moar speed: I can improve speed even without GPU shaders?
- [ ] Add turbulence: Moving a mouse thru sand piles should mix the sand.

### I'll forget this

```zsh
objdump -Sd zig-out/bin/falling_sand > junk/falling_sand.asm
```

### Observations

- The "if reduced" version of the cell update function (set_cell2) is on average a little bit faster than the "short circuit" version (set_cell1). Roughly 150 fps vs 140 fps, or in the neighborhood of a 7% improvement.
- On the other hand, falling_sand is over an order of magnitude slower than the game_of_life (16.5x). game_of_life is about 2500 fps while falling_sand is about 150 fps. Causes?
  1. Running over the array twice. For sure
  2. Out of order memory access. Probably, but I should be using at most 3 cache lines at a time? I should to look into this.
  3. Surprisingly, not the randomization. Tested, and any compute loss was negligible.
  4. Zig is probably vectorizing the update functions in the game_of_life.
  5. I'm probably not helping the situation with other subtle (or not) issues. Well, yea
