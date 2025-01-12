# Falling Sand

This classic simulation shows grains of colored sand falling. Drag the mouse (left button) across the window to spawn the sand grains.

I'm using this to familiarize myself with Zig and RayLib.

### TODO: If I ever get back to this

[ ] Add gravity: Umm.... Falling.
[ ] Use shaders: The algorithm is embarrassingly parallel.
[ ] Moar speed: I can improve speed even without shaders.
[ ] Add turbulence: Moving a mouse thru sand piles should mix the sand.

### I'll forget this

objdump -Sd zig-out/bin/falling_sand > junk/falling_sand.asm
