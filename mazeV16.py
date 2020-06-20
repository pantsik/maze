"""
Maze v.1.3
A search algorithm made in Python by Panos Tsikogiannopoulos  © 2020

Create a maze or load an existing one and let the explorer find the exit.
The explorer only knows the rooms he has been before. He can't see the exit and he can't see rooms that he has never been into.
White cells are empty rooms. Black cells are walls. The green cell is the starting point and the red cell is the finishing point.

Maze array cells interpratation:
Value:      0     1      2       3
Meaning:  empty  wall  start   finish

Route array cells interpratation:
Value:      0    90  180   270      9     1     
Meaning:  Right  Up  Left  Down   Empty  Wall

Basic exploration algorithm:
1. Search adjacent cells for the first empty cell
2. If found, move there and place the direction of the movement made to the new cell
3. Otherwise, move to the opposite of the current cell direction (backtracking)

I consider impossible for the explorer to run twice the maze's cells, i.e. steps > 2 * X_CELLS * Y_CELLS. Can you prove me wrong?
"""

# Import modules
from turtle import Turtle, Screen, setundobuffer, hideturtle, listen, onkeypress
import numpy as np
import time
import tkinter as tk
from tkinter import filedialog
import os

def maze_parameters():
    global xcells, ycells, cellsize, delayofmovement, show_how, explorers_path, xcells_int, ycells_int, cellsize_int, delayofmovement_float, show_how_string, explorers_path_string, window1
    window1 = tk.Tk()
    window1.after(1, lambda: window1.focus_force())
    window1.geometry("430x230")
    window1.title("Maze parameters")
    tk.Label(window1, text="  ").grid(row=0, column=0, sticky=tk.W)
    tk.Label(window1, text="Number of rooms Horizontally  ").grid(row=0, column=1, sticky=tk.W)
    tk.Label(window1, text="Number of rooms Vertically").grid(row=1, column=1, sticky=tk.W)
    tk.Label(window1, text="Room size in pixels").grid(row=2, column=1, sticky=tk.W)
    tk.Label(window1, text="Delay of movement in secs").grid(row=3, column=1, sticky=tk.W)
    tk.Label(window1, text="Show how to create a maze? (Y/N)     ").grid(row=4, column=1, sticky=tk.W)
    tk.Label(window1, text="Show explorer's path? (Y/N)").grid(row=5, column=1, sticky=tk.W)

    xcells = tk.Entry(window1, width=5)
    ycells = tk.Entry(window1, width=5)
    cellsize = tk.Entry(window1, width=5)
    delayofmovement = tk.Entry(window1, width=5)
    show_how = tk.Entry(window1, width=5)
    explorers_path = tk.Entry(window1, width=5)

    xcells.insert(0, xcells_int)
    ycells.insert(0, ycells_int)
    cellsize.insert(0, cellsize_int)
    delayofmovement.insert(0, delayofmovement_float)
    show_how.insert(0, show_how_string)
    explorers_path.insert(0, explorers_path_string)

    xcells.grid(row=0, column=2)
    ycells.grid(row=1, column=2)
    cellsize.grid(row=2, column=2)
    delayofmovement.grid(row=3, column=2)
    show_how.grid(row=4, column=2)
    explorers_path.grid(row=5, column=2)

    tk.Button(window1, text=" About maze ", command=about_maze).grid(row=7, column=1, sticky=tk.W, pady=20)
    tk.Button(window1, text=" Load maze ", command=load_maze).grid(row=7, column=1, sticky=tk.E, pady=20)
    tk.Button(window1, text=" Create maze ", command=window1.quit).grid(row=7, column=3, sticky=tk.E, pady=20)
    window1.mainloop()
    window1.withdraw()

def load_maze():
    global LOADED_BOARD, window1
    window1.quit()
    LOADED_BOARD = True

def about_maze():
    window2 = tk.Tk()
    window2.protocol('WM_DELETE_WINDOW', window2.quit)
    window2.geometry("960x410")
    window2.title("About Maze")
    tk.Label(window2, text=" Maze v.1.3", font="bold").grid(row=0, sticky=tk.W)
    tk.Label(window2, text="  A search algorithm made in Python by Panos Tsikogiannopoulos  © 2020").grid(row=1, sticky=tk.W)
    tk.Label(window2, text="  Create a maze or load an existing one and let the explorer find the exit.").grid(row=2, sticky=tk.W)
    tk.Label(window2, text="  White cells are empty rooms. Black cells are walls. The green cell is the starting point and the red cell is the finishing point.").grid(row=3, sticky=tk.W)
    tk.Label(window2, text=" ").grid(row=4, sticky=tk.W)
    tk.Label(window2, text="  Basic exploration algorithm:").grid(row=5, sticky=tk.W)
    tk.Label(window2, text="  1. Search adjacent rooms for the first unvisited room").grid(row=6, sticky=tk.W)
    tk.Label(window2, text="  2. If found, move there and place the direction of the movement made to the new room").grid(row=7, sticky=tk.W)
    tk.Label(window2, text="  3. Otherwise, move to the opposite of the current room direction (backtracking)").grid(row=8, sticky=tk.W)
    tk.Label(window2, text="  The explorer only knows the rooms he has seen before. He can't see the exit, the rooms that he has never passed by or the maze boundaries.").grid(row=9, sticky=tk.W)
    tk.Label(window2, text="  The explorer tries to find the exit in the fewest moves possible, given that he has no clue where to search first.").grid(row=10, sticky=tk.W)
    tk.Label(window2, text=" ").grid(row=11, sticky=tk.W)
    tk.Label(window2, text="  If you have any suggestions for improvements, contact me at pantsik@yahoo.gr").grid(row=12, sticky=tk.W)
    tk.Button(window2, text=" OK ", command=window2.quit).grid(row=13, column=0, sticky=tk.N, pady=20)
    window2.mainloop()
    window2.withdraw()
    
def maze_info():
    window3 = tk.Tk()
    window3.after(1, lambda: window3.focus_force())
    window3.protocol('WM_DELETE_WINDOW', window3.quit)
    window3.geometry("650x250")
    window3.title("How to create a maze")
    tk.Label(window3, text=" How to create a maze:", font="bold").grid(row=0, sticky=tk.W)
    tk.Label(window3, text="  Move the blue cell around with the arrow keys ← → ↑ ↓").grid(row=1, sticky=tk.W)
    tk.Label(window3, text="  Place a wall with the SPACE BAR key. Remove a wall with the Left Control key (Ctrl).").grid(row=2, sticky=tk.W)
    tk.Label(window3, text="  Change the starting position with the F1 key. Change the finishing position with the F2 key.").grid(row=3, sticky=tk.W)
    tk.Label(window3, text="  Finish your maze and let the explorer find the exit with the Esc key.").grid(row=4, sticky=tk.W)
    tk.Label(window3, text="  Save your maze with the 's' key.").grid(row=5, sticky=tk.W)
    tk.Label(window3, text="  Cancel your maze with the Delete key.").grid(row=6, sticky=tk.W)
    tk.Button(window3, text=" OK ", command=window3.quit).grid(row=7, column=0, sticky=tk.N, pady=20)
    window3.mainloop()
    window3.withdraw()

def input_error():
    window4 = tk.Tk()
    window4.protocol('WM_DELETE_WINDOW', window4.quit)
    window4.geometry("340x100")
    window4.title("Error")
    tk.Label(window4, text=" Non-numerical or non-integer values entered.").grid(row=0, sticky=tk.W)
    tk.Button(window4, text=" OK ", command=window4.quit).grid(row=1, column=0, sticky=tk.N, pady=20)
    window4.mainloop()
    window4.withdraw()

def exit_found():
    global step, shortest_route
    window5 = tk.Tk()
    window5.protocol('WM_DELETE_WINDOW', window5.quit)
    window5.geometry("310x160")
    window5.title("Exit found!")
    w1 = tk.Label(window5, text=" ")
    w2 = tk.Label(window5, text="Exit found in " + str(step) + " steps.")
    w3 = tk.Label(window5,  fg="blue", text="Shortest route found was " + str(shortest_route) + " steps away.")
    w4 = tk.Label(window5, text=" ")
    w5 = tk.Button(window5, text=" OK ", command=window5.quit)
    w1.pack()
    w2.pack()
    w3.pack()
    w4.pack()
    w5.pack()
    window5.mainloop()
    window5.withdraw()

def no_exit_found():
    window6 = tk.Tk()
    window6.protocol('WM_DELETE_WINDOW', window6.quit)
    window6.geometry("310x130")
    window6.title("No exit found")
    w1 = tk.Label(window6, text=" ")
    w2 = tk.Label(window6, text="No exit found.")
    w3 = tk.Label(window6, text=" ")
    w4 = tk.Button(window6, text=" OK ", command=window6.quit)
    w1.pack()
    w2.pack()
    w3.pack()
    w4.pack()
    window6.mainloop()
    window6.withdraw()

def save_file():
    global maze, X_CELLS, Y_CELLS, step

    application_window = tk.Tk()
    application_window.withdraw()

    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [("maze files", ".maz")]

    # Ask the user to select a single file name for saving.
    filename = filedialog.asksaveasfilename(parent=application_window,
                                          initialdir=os.getcwd(),
                                          title="Please select a file name for saving:",
                                          filetypes=my_filetypes)
    if len(filename) != 0:
        if filename[-4:] != ".maz":
            filename += ".maz"
        f = open(filename, "w")
        f.write(str(X_CELLS) + "," + str(Y_CELLS) + "\n")
        for j in range(Y_CELLS):
            for i in range(X_CELLS):
                f.write(str(maze[j, i]))
            f.write("\n")
        if step == 0:
            f.write("No exit found yet.")
        else:
            f.write("Exit found in " + str(step) + " steps.")
        f.close()

def load_file():
    global X_CELLS, Y_CELLS, maze_loaded, filename, LOADED_BOARD

    window1.quit()
    application_window = tk.Tk()
    application_window.withdraw()

    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [("maze files", ".maz")]

    # Ask the user to select a single file name.
    filename = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)
    if len(filename) != 0:
        f = open(filename, "r")
        header = f.read()
        coma_place = header.find(",")
        X_CELLS = int(header[:coma_place])
        linebreak_place = header.find("\n")
        Y_CELLS = int(header[coma_place+1:linebreak_place])
        maze_loaded = np.zeros((Y_CELLS, X_CELLS), np.int8)
        data = header[linebreak_place+1:]
        d = 0
        for j in range(Y_CELLS):
            for i in range(X_CELLS):
                maze_loaded[j, i] = int(data[d])
                d += 1
            d += 1
        f.close()

def setup_turtles():
    global pen, wall, exp
    
    # Setup grid turtle
    pen = Turtle()
    pen.speed(0)
    pen.pensize(GRID_LINE)
    pen.color(GREY)

    # Setup wall turtle
    wall = Turtle()
    wall.speed(0)
    wall.color("blue")
    wall.shape("square")

    # Setup explorer turtle
    exp = Turtle()
    exp.shape("arrow")
    exp.speed(0)
    exp.color("orange")
    exp.pensize(3)
    exp.setheading(0)
    exp.penup()
    exp.hideturtle()

def draw_grid():
    for i in range(Y_CELLS+1):  # Draw horizontal lines
        pen.penup()
        pen.setposition(-SCREEN_WIDTH/2 + 10, (SCREEN_HEIGHT/2 - 10) - CELL_SIZE*i)
        pen.pendown()
        pen.fd(X_CELLS*CELL_SIZE)
    pen.rt(90) # turn pen 90 degrees right
    for i in range(X_CELLS+1):  # Draw vertical lines
        pen.penup()
        pen.setposition(-SCREEN_WIDTH/2 + 10 + CELL_SIZE*i, (SCREEN_HEIGHT/2 - 10))
        pen.pendown()
        pen.fd(Y_CELLS*CELL_SIZE)
    pen.hideturtle()
    wall.penup()
    wn.update()

def move_left():
    global x_wall, x, drawing
    if drawing:
        if x_wall > -(SCREEN_WIDTH-CELL_SIZE)/2 + 10:
            x_wall -= CELL_SIZE
            x -= 1

def move_right():
    global x_wall, x, drawing
    if drawing:
        if x_wall < -(SCREEN_WIDTH-CELL_SIZE)/2 + 10 + (X_CELLS - 1) * CELL_SIZE:
            x_wall += CELL_SIZE
            x += 1

def move_up():
    global y_wall, y, drawing
    if drawing:
        if y_wall < (SCREEN_HEIGHT-CELL_SIZE)/2 - 10:
            y_wall += CELL_SIZE
            y -= 1

def move_down():
    global y_wall, y, drawing
    if drawing:
        if y_wall > (SCREEN_HEIGHT-CELL_SIZE)/2 - 10 - (Y_CELLS - 1) * CELL_SIZE:
            y_wall -= CELL_SIZE
            y += 1

def build_wall():
    global x_wall, y_wall, x, y, drawing
    if drawing:
        pen.color("black")
        pen.penup()
        pen.setposition(x_wall + CELL_SIZE/2 - GRID_LINE, y_wall + CELL_SIZE/2 - GRID_LINE)
        pen.pendown()
        pen.begin_fill()
        for i in range(4):  # Draw a square
            pen.fd(CELL_SIZE - 2*GRID_LINE)
            pen.rt(90)
        pen.end_fill()    # Fill the square
        maze[y, x] = 1

def remove_wall():
    global x_wall, y_wall, x, y, drawing
    if drawing:
        pen.color(GREY, "white")
        pen.penup()
        pen.setposition(x_wall + CELL_SIZE/2, y_wall + CELL_SIZE/2)
        pen.pendown()
        pen.begin_fill()
        for i in range(4):  # Draw a square
            pen.fd(CELL_SIZE)
            pen.rt(90)
        pen.end_fill()    # Fill the square
        maze[y, x] = 0

def set_start_cell():
    global x_wall, y_wall, x, y, start_x, start_y, start_x_wall, start_y_wall, drawing
    if drawing:
        # Removes previous starting cell
        if start_x != -1 and start_y != -1:
            pen.color(GREY, "white")
            pen.penup()
            pen.setposition(start_x_wall, start_y_wall)
            pen.pendown()
            pen.begin_fill()
            for i in range(4):  # Draw a square
                pen.fd(CELL_SIZE)
                pen.rt(90)
            pen.end_fill()    # Fill the square
            maze[start_y, start_x] = 0

        # Sets current starting cell
        pen.color("green")
        pen.penup()
        pen.setposition(x_wall + CELL_SIZE/2 - GRID_LINE, y_wall + CELL_SIZE/2 - GRID_LINE)
        pen.pendown()
        pen.begin_fill()
        for i in range(4):  # Draw a square
            pen.fd(CELL_SIZE - 2*GRID_LINE)
            pen.rt(90)
        pen.end_fill()    # Fill the square
        start_x = x
        start_y = y
        start_x_wall = x_wall + CELL_SIZE/2
        start_y_wall = y_wall + CELL_SIZE/2
        maze[start_y, start_x] = 2

def set_finish_cell():
    global x_wall, y_wall, x, y, finish_x, finish_y, finish_x_wall, finish_y_wall, drawing
    if drawing:
        # Removes previous finishing cell
        if finish_x != -1 and finish_y != -1:
            pen.color(GREY, "white")
            pen.penup()
            pen.setposition(finish_x_wall, finish_y_wall)
            pen.pendown()
            pen.begin_fill()
            for i in range(4):  # Draw a square
                pen.fd(CELL_SIZE)
                pen.rt(90)
            pen.end_fill()    # Fill the square
            maze[finish_y, finish_x] = 0

        # Sets current finishing cell
        pen.color("red")
        pen.penup()
        pen.setposition(x_wall + CELL_SIZE/2 - GRID_LINE, y_wall + CELL_SIZE/2 - GRID_LINE)
        pen.pendown()
        pen.begin_fill()
        for i in range(4):  # Draw a square
            pen.fd(CELL_SIZE - 2*GRID_LINE)
            pen.rt(90)
        pen.end_fill()    # Fill the square
        finish_x = x
        finish_y = y
        finish_x_wall = x_wall + CELL_SIZE/2
        finish_y_wall = y_wall + CELL_SIZE/2
        maze[finish_y, finish_x] = 3

def end_of_drawing():
    global drawing
    drawing = False
    wall.hideturtle()
    wn.update()

def load_board():
    global maze, maze_loaded, x, y, x_wall, y_wall, start_x, start_y, finish_x, finish_y

    maze = maze_loaded
    wall.hideturtle()
    for j in range(Y_CELLS):
        x_wall = -(SCREEN_WIDTH-CELL_SIZE)/2 + 10   # Set the X-axis center of wall-turtle in pixels
        for i in range(X_CELLS):
            if maze[j, i] == 1:
                x = i
                y = j
                build_wall()
            elif maze[j, i] == 2:
                x = i
                y = j
                set_start_cell()
                start_x = i
                start_y = j
            elif maze[j, i] == 3:
                x = i
                y = j
                set_finish_cell()
                finish_x = i
                finish_y = j
            x_wall += CELL_SIZE
        y_wall -= CELL_SIZE

    wn.update()
    x_wall = -(SCREEN_WIDTH-CELL_SIZE)/2 + 10   # Set the X-axis center of wall-turtle in pixels
    y_wall = (SCREEN_HEIGHT-CELL_SIZE)/2 - 10   # Set the Y-axis center of wall-turtle in pixels
    x, y = 0, 0

def restart_maze():
    global restart
    restart = True

def keyboard_bindings():
    # Create keyboard bindings
    listen()
    onkeypress(move_left, "Left")
    onkeypress(move_right, "Right")
    onkeypress(move_up, "Up")
    onkeypress(move_down, "Down")
    onkeypress(build_wall, "space")
    onkeypress(remove_wall, "Control_L")
    onkeypress(set_start_cell, "F1")
    onkeypress(set_finish_cell, "F2")
    onkeypress(end_of_drawing, "Escape")
    onkeypress(save_file, "s")
    onkeypress(restart_maze, "Delete")

def isolation_score(dir1, y1, x1):    # 0 = least isolated, 3 = most isolated
    global route, X_CELLS, Y_CELLS
    score = 0

    if dir1 != "down":   # Don't check the direction it came from because it is visited
        j = y1
        wall_found = 0
        while j > -1 and (route[j, x1] == 9 or route[j, x1] == 1):
            if route[j, x1] == 1 and wall_found == 0:
                wall_found = y1 - j
            j -= 1
        if j == -1 and wall_found == 0:     # Not visited up before
            #print("isolation score up:", 0)
            return 0
        elif j == -1 and wall_found > 0:    # Found wall up but not visited up before
            score += 1 / (10 * wall_found)
            #print("wall dist:", wall_found, "isolation score wall up:", score)
        elif j > -1:     # Found visited path up
            score += 1 / (y1 - j)
            #print("route dist:", y1 - j, "isolation score route up:", score)

    if dir1 != "up":   # Don't check the direction it came from because it is visited
        j = y1
        wall_found = 0
        while j < Y_CELLS and (route[j, x1] == 9 or route[j, x1] == 1):
            if route[j, x1] == 1 and wall_found == 0:
                wall_found = j - y1
            j += 1
        if j ==  Y_CELLS and wall_found == 0:     # Not visited down before
            #print("isolation score down:", 0)
            return 0
        elif j == Y_CELLS and wall_found > 0:    # Found wall down but not visited down before
            score += 1 / (10 * wall_found)
            #print("wall dist:", wall_found, "isolation score wall down:", score)
        elif j < Y_CELLS:     # Found visited path down
            score += 1 / (j - y1)
            #print("route dist:", j - y1, "isolation score route down:", score)

    if dir1 != "right":   # Don't check the direction it came from because it is visited
        i = x1
        wall_found = 0
        while i > -1 and (route[y1, i] == 9 or route[y1, i] == 1):
            if route[y1, i] == 1 and wall_found == 0:
                wall_found = x1 - i
            i -= 1
        if i == -1 and wall_found == 0:     # Not visited left before
            #print("isolation score left:", 0)
            return 0
        elif i == -1 and wall_found > 0:    # Found wall left but not visited left before
            score += 1 / (10 * wall_found)
            #print("wall dist:", wall_found, "isolation score wall left:", score)
        elif i > -1:     # Found visited path left
            score += 1 / (x1 - i)
            #print("route dist:", x1 - i, "isolation score route left:", score)

    if dir1 != "left":   # Don't check the direction it came from because it is visited
        i = x1
        wall_found = 0
        while i < X_CELLS and (route[y1, i] == 9 or route[y1, i] == 1):
            if route[y1, i] == 1 and wall_found == 0:
                wall_found = i - x1
            i += 1
        if i == X_CELLS and wall_found == 0:     # Not visited right before
            #print("isolation score right:", 0)
            return 0
        elif i == X_CELLS and wall_found > 0:    # Found wall right but not visited right before
            score += 1 / (10 * wall_found)
            #print("wall dist:", wall_found, "isolation score wall right:", score)
        elif i < X_CELLS:     # Found visited path right
            score += 1 / (i - x1)
            #print("route dist:", i - x1, "isolation score route right:", score)

    return score
    

# Set constants
GREY = (0.8, 0.8, 0.8)
GRID_LINE = 1
first_run = True
xcells_int = 20
ycells_int = 10
cellsize_int = 50
delayofmovement_float = 0.2
show_how_string = "Y"
explorers_path_string = "Y"
filename = ""
MAX_ROOMS = 10000
LOADED_BOARD = False

while True:
    maze_parameters()

    try:
        X_CELLS = int(xcells.get())
        xcells_int = xcells.get()
        Y_CELLS = int(ycells.get())
        ycells_int = ycells.get()
        CELL_SIZE = int(cellsize.get())
        cellsize_int = cellsize.get()
        DELAY = float(delayofmovement.get())
        delayofmovement_float = delayofmovement.get()

        if show_how.get() == "Y" or show_how.get() == "y" or show_how.get() == "yes" or show_how.get() == "Yes" or show_how.get() == "YES":
            show_how_string = "Y"
        else:
            show_how_string = "N"
        if explorers_path.get() == "Y" or explorers_path.get() == "y" or explorers_path.get() == "yes" or explorers_path.get() == "Yes" or explorers_path.get() == "YES":
            explorers_path_string = "Y"
            SHOW_PATH = True
        else:
            explorers_path_string = "N"
            SHOW_PATH = False

        if LOADED_BOARD:
            load_file()
            if len(filename) == 0:
                LOADED_BOARD = False
                continue

            
        # Setup screen
        SCREEN_WIDTH = X_CELLS*CELL_SIZE + 50
        SCREEN_HEIGHT = Y_CELLS*CELL_SIZE + 50
        if first_run:
            first_run = False
        else:
            wn.clearscreen()
        keyboard_bindings()
        wn = Screen()
        wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, startx=0, starty=0)
        wn.screensize(SCREEN_WIDTH, SCREEN_HEIGHT)
        wn.bgcolor("white")
        wn.title("Maze")
        wn.tracer(0, 0)
        setup_turtles()
        wn.update()

        # Set variables
        wall.shapesize(CELL_SIZE/20, CELL_SIZE/20)
        exp.shapesize(CELL_SIZE*0.04)
        maze = np.zeros((Y_CELLS, X_CELLS), np.int8)    # Create a 2D array filled with zeroes which represents the maze
        route = np.zeros((Y_CELLS, X_CELLS), np.int16)  # Create a 2D array filled with 9s which represents the route that has been explored so far.
        route.fill(9)
        drawing = True
        x_wall = -(SCREEN_WIDTH-CELL_SIZE)/2 + 10   # Set the X-axis center of wall-turtle in pixels to the start of the grid
        y_wall = (SCREEN_HEIGHT-CELL_SIZE)/2 - 10   # Set the Y-axis center of wall-turtle in pixels to the start of the grid
        start_x_wall = x_wall + CELL_SIZE/2
        start_y_wall = y_wall + CELL_SIZE/2
        finish_x_wall = x_wall + CELL_SIZE/2
        finish_y_wall = y_wall + CELL_SIZE/2
        x, y  = 0, 0   # Set the X-axis and Y-axis of Array in array dimensions
        start_x, start_y, finish_x, finish_y = -1, -1, -1, -1   # Set the X-axis and Y-axis of Array in array dimensions
        step, shortest_route = 0, 0
        restart = False

        draw_grid()
        if LOADED_BOARD:
            LOADED_BOARD = False
            load_board()
        else:
            # Set start, finish, pen initial positions
            set_start_cell()
            x_wall += (X_CELLS-1)*CELL_SIZE   # Set the X-axis center of wall-turtle to the grid end
            y_wall -= (Y_CELLS-1)*CELL_SIZE   # Set the Y-axis center of wall-turtle to the grid end
            x = X_CELLS - 1     # Set the x cordinate of the maze array to the right end
            y = Y_CELLS - 1     # Set the y cordinate of the maze array to the bottom end
            set_finish_cell()
            x_wall = -(SCREEN_WIDTH-CELL_SIZE)/2 + 10 + CELL_SIZE   # Set the X-axis center of wall-turtle to the second cell
            y_wall = (SCREEN_HEIGHT-CELL_SIZE)/2 - 10   # Set the Y-axis center of wall-turtle to the first cell
            x = 1 # Set the x cordinate of the maze array to the second place
            y = 0 # Set the y cordinate of the maze array to the first place

        # Draw maze
        wall.showturtle()
        wall.setposition(x_wall, y_wall)
        wn.update()
        if show_how_string == "Y":
            maze_info()
        while drawing and not restart:
            wall.setposition(x_wall, y_wall)
            wn.update()

        #print("Maze:")
        #print(maze)

        # set up variables before main exploration loop
        exp.setposition(start_x_wall  - CELL_SIZE/2, start_y_wall - CELL_SIZE/2)
        if SHOW_PATH: # Leave the explorer's trace behind
            exp.pendown()
        else:
            exp.penup()
        exp.showturtle()
        if start_x == -1 and start_y == -1:
            start_x, start_y = 0, 0
        x = start_x
        y = start_y
        new_direction = 0
        route[start_y, start_x] = new_direction     # Although the direction from the previous cell is set to the new cell, the starting cell is the only exception.


        while not restart:     # Main exploration loop
            backtrack = False
            exp.pencolor("blue")
            wn.update()
            time.sleep(DELAY)
            
            if maze[y, x] == 3: # exit cell found
                print()
                print("Exit found in", step, "steps.")
                print("Shortest route found was", shortest_route, "steps away.")
                print()
                exit_found()
                break

            d_right, d_left, d_up, d_down = MAX_ROOMS, MAX_ROOMS, MAX_ROOMS, MAX_ROOMS

            if x < X_CELLS-1 and maze[y, x+1] != 1 and route[y, x+1] == 9:  # Check right for the distance from start. Diagonal distances are prefered over straight ones.
                d_hor = abs(x+1 - start_x)
                d_ver = abs(y - start_y)
                d_hor_ver = abs(d_hor - d_ver)
                d_right = (3 - isolation_score("right", y, x+1)**2) * (d_hor + d_ver + d_hor_ver / MAX_ROOMS)
            else:
                if x < X_CELLS-1 and route[y, x+1] == 9:  # There is a wall to the right
                    route[y, x+1] = 1

            if x > 0 and maze[y, x-1] != 1 and route[y, x-1] == 9:  # Check left for the distance from start. Diagonal distances are prefered over straight ones.
                d_hor = abs(x-1 - start_x)
                d_ver = abs(y - start_y)
                d_hor_ver = abs(d_hor - d_ver)
                d_left = (3- isolation_score("left", y, x-1)**2) * (d_hor + d_ver + d_hor_ver / MAX_ROOMS)
            else:
                if x > 0 and route[y, x-1] == 9:  # There is a wall to the left
                    route[y, x-1] = 1

            if y < Y_CELLS-1 and maze[y+1, x] != 1 and route[y+1, x] == 9:  # Check down for the distance from start. Diagonal distances are prefered over straight ones.
                d_hor = abs(x - start_x)
                d_ver = abs(y+1 - start_y)
                d_hor_ver = abs(d_hor - d_ver)
                d_down = (3 - isolation_score("down", y+1, x)**2) * (d_hor + d_ver + d_hor_ver / MAX_ROOMS)
            else:
                if y < Y_CELLS-1 and route[y+1, x] == 9:
                    route[y+1, x] = 1

            if y > 0 and maze[y-1, x] != 1 and route[y-1, x] == 9:  # Check up for the distance from start. Diagonal distances are prefered over straight ones.
                d_hor = abs(x - start_x)
                d_ver = abs(y-1 - start_y)
                d_hor_ver = abs(d_hor - d_ver)
                d_up = (3 - isolation_score("up", y-1, x)**2) * (d_hor + d_ver + d_hor_ver / MAX_ROOMS)
            else:
                if y > 0  and route[y-1, x] == 9:
                    route[y-1, x] = 1

            # print(route)
            # print("d_right:", d_right, "d_left:", d_left, "d_down:", d_down, "d_up:", d_up)

            path_found = False
            check_loop = 0  # Tries all 4 new directions for the one that is not the same with the previous direction
            while check_loop < 4:
                if d_right == min(d_right, d_left, d_down, d_up) and d_right != MAX_ROOMS and new_direction == 0:  # Check right and follow that path if the explorer has passed closer in that direction before than any other directions
                    direction = 0
                    route[y, x+1] = 0
                    x += 1
                    path_found = True
                    break
                if d_up == min(d_right, d_left, d_down, d_up) and d_up != MAX_ROOMS and new_direction == 90:  # Check up and follow that path if the explorer has passed closer in that direction before than any other directions
                    direction = 90
                    route[y-1, x] = 90
                    y -= 1
                    path_found = True
                    break
                if d_left == min(d_right, d_left, d_down, d_up) and d_left != MAX_ROOMS and new_direction == 180:  # Check left and follow that path if the explorer has passed closer in that direction before than any other directions
                    direction = 180
                    route[y, x-1] = 180
                    x -= 1
                    path_found = True
                    break
                if d_down == min(d_right, d_left, d_down, d_up) and d_down != MAX_ROOMS and new_direction == 270:  # Check down and follow that path if the explorer has passed closer in that direction before than any other directions
                    direction = 270
                    route[y+1, x] = 270
                    y += 1
                    path_found = True
                    break
                new_direction += 90 # Changes the new direction trying to move to a different direction than the previous one, so that the explorer does not move too far away from the already explored rooms.
                if new_direction == 360:
                    new_direction = 0
                check_loop += 1
            
            if not path_found:      # Backtracking
                backtrack = True
                exp.pencolor("red")
                # print("Nowhere to go. Backtracking...")
                if x == start_x and y == start_y:
                    print("No exit found.")
                    no_exit_found()
                    break
                else:
                    # change direction 180 degrees
                    direction = route[y, x]
                    direction = direction - 180
                    if direction == 90:
                        y -= 1
                    elif direction == 0:
                        x += 1
                    elif direction == -180:
                        direction = 180
                        x -= 1
                    else:   # direction = -90
                        direction = 270
                        y += 1
                    
            exp.setheading(direction)
            exp.forward(CELL_SIZE)
            step += 1
            new_direction = direction + 90
            if new_direction == 360:
                new_direction = 0
            if not backtrack:
                shortest_route += 1
            else:
                shortest_route -= 1
            # print("step:",step, " shortest route:",shortest_route)

    except ValueError:
        input_error()
        continue

