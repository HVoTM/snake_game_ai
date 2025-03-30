import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# pygame setup
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

"""List of additional features for Reinforcement Learning
    - A function to reset
    - implementations of reward
    - change play_step() function to take in the action and compute the next action
    - game_iteration: a function to keep track of the iteration
    - is_collision
    Returns:
        _type_: _description_
"""
# setting directional keys for interaction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors to set for graphics
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE2 = (124, 255, 0)
BLUE1 = (0, 128, 0)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20 # set pixel size to 20
SPEED = 15

class SnakeGame:
    # set display resolution
    def __init__(self, w=640, h=480) -> None:
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game!')
        self.clock = pygame.time.Clock()
        
        self.newgame()

    # function to reset the game into a new one for the AI agent to hit reset if died
    def newgame(self) -> None:
        # init game state, starting with going to the right
        self.direction = Direction.RIGHT
        
        # set the head in the middle of the screen
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,  # we init the head going to the right, so we should move the body by 2 block sizes
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 # reset new game so frame iteration back to 0

    def _place_food(self):
        # get a random int with pixel length being scaled
        # after we acquire a random pixel coordinate, we multiply by BLOCK_SIZE
        # again to achieve the block
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake: # making sure the food is not place in the snake
            self._place_food()
    
    # the main function to implement moves and update directions on display   
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # command used to exit in Python
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head) # for every screen frame, just iteratively insert the new head
        # then we have a code snippet to pop the head in section 4 of this function
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration  > 100*len(self.snake): # second clause to make sure if the snake is going on
                                                                                # without getting a reward or dying -> we reset the game
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1 # if food is eaten, then we skip the pop() method and a new section of the body is going to be
                            # inserted in the next frame refresh -> this is how the body will get longer
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def _is_collision(self, point=None):
        if point is None:
            point = self.head
        # check if snake hits the boundaries
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        # check if snake hits itself
        if point in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+2, pt.y+2, 16, 16))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # flip() the display to put work on screen
        
    def _move(self, action):
        "action vector [straight, right, left]"

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP] # create a list corresponding to Direction class
        index = clock_wise.index(self.direction) # get a variable to get the index of these values

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[index] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (index +  1) % 4
            new_direction = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: #[0, 0, 1]
            next_idx = (index -1) % 4 # go counter clockwise
            new_direction = clock_wise[index] # left turn r -> u -> l -> d

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        # checking the direction, continuously updating the positionings of the head
        # update to class attribute head and we will have insert() function above to add the new head
        self.head = Point(x, y)

"Remove the __main__ call, b'cuz we are going to use the agent to implement the move"