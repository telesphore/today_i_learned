# The classic cellular automaton

- This version is in C, which has advantages and disadvantages.
  - Disadvantage: Many many foot-guns.
  - Advantage: Learning resources are plentiful.
- The Game of Life grid is being treated as a torus.
  - This complicates using SIMD, but, hey, it's a learning exercise.

I'm leaning on rayLib for the graphics.
