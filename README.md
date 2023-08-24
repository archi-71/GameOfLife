# GameOfLife

This project simulates the cellular automaton [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), written in Python with the pygame library.

The game is played on a 2D grid of cells, where each cell is either 'alive' (displayed in white) or 'dead' (displayed in black). Upon each iteration of the game, rules are applied to each cell of the grid to determine if a cell's state should change. For the game of life, if a living cell has fewer than 2 or more than 3 neighbours, the cell dies, and if a dead cell has exactly 3 neighbours, it becomes alive. These simplistic rules can give rise to vastly complex and chaotic behaviour, where seemingly random configurations of cells evolve into symmetrical patterns and structures. This simulation allows the user to draw and erase live cells on the grid by dragging with the mouse. The automaton can then be run using the 'start'/'stop' button, and reset back to a blank grid with the 'reset' button.

![image](https://github.com/archi-71/GameOfLife/assets/70474549/516c8aab-38ea-4501-bba0-807f8b6ea236)
![image](https://github.com/archi-71/GameOfLife/assets/70474549/c1841a2f-fba9-473d-adc0-27b471877435)

