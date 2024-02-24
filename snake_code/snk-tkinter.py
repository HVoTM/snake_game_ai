"""
--------------------------------------------------------------------------
                    SNAKE XENZIA GAME
--------------------------------------------------------------------------
Written in Python and tkinter module package
Name: HUNG VO
source: Bro Code
"""
from tkinter import *
from tkinter import ttk 
import random

# Create some glonbal constant variables for game settings
GAME_WIDTH = 1000 # unit: pixel
GAME_HEIGHT = 600
SPEED = 50 # lower the number, the faster the game 
SPACE_SIZE = 40 # how large are the items (food, body parts)
BODY_PARTS = 3 # intial size of the snake 
SNAKE_COLOR = "#4a8c55"
FOOD_COLOR = "#eb4334"
BACKGROUND_COLOR = "#c7cc7a"

# Classes for objects creation in the game
class Snake:
    # define instance method to initialize object Snake
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        # initialize the list of coordinates for the corresponding body parts
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0]) # snake start at the top left corner
        # create squares for each body parts using canvas.create_rectangle()
        for x, y in self.coordinates: # x, y for list of lists
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Create a class for Food
class Food:
    def __init__(self):
        # create Food object at a random coordinate given the space
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE # GAME_WIDTH / SPACE_SIZE: RELATIVE SIZE BETWEEN THE GAME AND ITEM PARTICLE
                                                                        # OR A BLOCK FROM THE ITEM
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        
        # canvas call name to be interacting with creating, modifying, and removing items on the screen
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    x, y = snake.coordinates[0] # the head of the snake

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # given a direction, the snake will continuously grow the head and remove the tail
    # To make sure you understand if the snake will not extend!
    # insert() method will do the trick, as it will prepend and push the remaining part of the list back by one position.
    # and by deleting the tail by indexing the list by -1 every iteration of next_turn, it will not extend the body.
    snake.coordinates.insert(0, (x, y)) 
    # create a new graphic for the head of the snake
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # set to check if the head of the snake will coincide with the coordinate of the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1 # call and update
        label.config(text="Score:{}".format(score)) # config() to update score

        canvas.delete("food")
        food = Food() # inititate a new food somewhere else random

    else:
        # delete the last square in the body if food is not eaten
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food) # call function again once after SPEED time.

def change_direction(new_direction):
    # set as global for other functions
    global direction

    if new_direction == 'left':
        if direction != 'right': # we will refrain from using 180 degree turn
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]: # everything after the head of the snake
        if x == body_part[0] and y == body_part[1]: # body_part[0] for x-coord, body_part[1] for y-coord of that body_part
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('comicsans',70), text="GAME OVER", fill="red", tag="gameover")

# Additional features to be added to the game
def replay():
    global snake, food, score, direction

    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)

def wall_warp(): # adding function for the snake to warp to the other side of the wall
    pass

# Tcl codelines...
window = Tk()
window.title("Snake Xenzia")
window.resizable(False, False) # instruct window manager not to resize the window height and width after setting it once    

score = 0
direction = 'down' # direction is set global up there 

# Create Widgets for GUI: label
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack() # after done with configuration, pack into parent widget using pack()  

# Create Canvas widget for GUI
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# added restart button for replay

restart_button = Button(window, text="Replay", command=replay, font=('consolas', 20), bg="#fcba03")
restart_button.place(x=2, y=2)

window.update() # update(): update the window so that it renders

# Now we will try to center the screenplay.
# Acquire ratio and measurements of the widget info and screen 
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# get x and y to see how much we need to adjust the position of the window
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# call geometry() to set or retrieve the dimensions and position of the window
window.geometry(f"{window_width}x{window_height}+{x}+{y}") # x and y must be integer, not float 

# bind() to create call on the program upon interacting with the arrow keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create interactive objects and call on next_turn 
snake = Snake()
food = Food()

next_turn(snake, food)

# Calling mainloop on the package to prevent from terminating the screen after finishing
window.mainloop()