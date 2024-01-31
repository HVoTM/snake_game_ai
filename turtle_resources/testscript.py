# Introduction to turtle
import turtle as t 
from random import random

# set background color
t.bgcolor("black")
# define object-oriented screen and set its title
scr = t.Screen()
scr.title("Animation Circle ")

# create OOP of Turtle to call functions via its distribution
turtle=t.Turtle()
turtle.color("orange")
turtle.speed(0) # set to 0 for fastest

# call hideturtle() to make it invisible
turtle.hideturtle() 

for i in range(500):
    # call to create circle with double the size of every increment
    turtle.circle(i*2)
    turtle._rotate(5)

t.mainloop() # mainloop at the end to stop the screen for terminating after finishing