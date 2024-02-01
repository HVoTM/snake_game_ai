from tkinter import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#4a8c55"
FOOD_COLOR = "#eb4334"
BACKGROUND_COLOR = "#c7cc7a"

window = Tk() # call Tk (a Tcl package to create and manipulate GUI widgets) with a namespace
window.title('Test GUI')
window.resizable(False, False)

score = 0

label = Label(window, text="Something here:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()


window.mainloop()