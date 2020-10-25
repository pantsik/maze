# Maze
A search algorithm made in Python by Panos Tsikogiannopoulos  © 2020.

Create a maze or load an existing one and let the explorer find the exit.
White cells are empty rooms. Black cells are walls. The green cell is the starting point and the red cell is the finishing point.

Basic exploration algorithm:
1. Search adjacent rooms for the first unvisited room
2. If found, move there and place the direction of the movement made to the new room
3. Otherwise, move to the opposite of the current room direction (backtracking)

The explorer only knows the rooms he has seen before. He can't see the exit, the rooms that he has never passed by or the maze boundaries.
The explorer tries to find the exit in the fewest moves possible, given that he has no clue where to search first.

If you have any suggestions for improvements, contact me at pantsik2@gmail.com

User instructions:

1. This is a windows application.
2. You must have any version of Python installed on your computer.
3. Run the MAZE.py file. It will open a menu which contains commands and directions.
4. Files with the extension .maz in this repo are mazes that can be loaded and explored. You can design your own mazes and save them as .maz files also.
