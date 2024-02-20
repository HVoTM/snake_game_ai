# Snake Game

Introductory project in developing the classical game in our nostalgic cellphone device - Snake or Xenzia Snake

We will develop via Python mainly with the help of __tkinter__ module: https://docs.python.org/3/library/tkinter.html
## tkinter (Tk interface)
> standard Python interface to the Tcl/Tk GUI toolkit.
run: `python -m tkinter` in CLI to demonstrate a simple Tk interface

> ADDITIONAL: for further info on using tkinter: https://docs.python.org/3/library/tkinter.html#important-tk-concepts
> ADDITIONAL PROJECT: [tic-tac-toe using tkinter](https://realpython.com/tic-tac-toe-python/) 

# Main improvements in addition to the other default settings
1. adding space warp, which will teleport over to the opposing wall if we hit
    + basically remove the collisions on the wall, and just set it to the body itself
2. Defining other packages for theme and design
3. AI: define a self-playing snake to play the game until out of space to traverse.

# Train an AI to play Snake
Here we will be working on implementing an AI agent for self-learning on the Snake Game

We will be working on Pygame and using Deep Q Learning - a Deep Learning technique - to create an agent for this AI to learn and play.

## Steps for implementation
1. Theory
2. Implement the game(environment)
3. Implement the agent
4. Implement the model

# Resources
Tutorial: https://www.youtube.com/watch?v=L8ypSXwyBds&list=PLkZkb1B52EOdC-ZagCo7LrxxNuoawM1HQ&index=38&ab_channel=freeCodeCamp.org
