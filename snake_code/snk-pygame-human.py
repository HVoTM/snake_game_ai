import pygame
import random
from enum import Enum
from collections import namedtuple
# pygame setup
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

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
SPEED = 18

class SnakeGame:
    # set display resolution
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game!')
        self.clock = pygame.time.Clock()
        
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
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # command used to exit in Python
            if event.type == pygame.KEYDOWN: # pygame.KEYDOWN is to check if there is any key pressed on the keyboard
                # We add a second argument to check if the current direction of the class SnakeGame is on the opposite
                # if it is opposite, we will not update the direction to avoid collisions
                # NOTE: MAYBE just leave it as be should be fine, as another element for the agent to take into consideration when moving
                if (event.key == pygame.K_LEFT) & (self.direction != Direction.RIGHT):
                    self.direction = Direction.LEFT
                elif (event.key == pygame.K_RIGHT) & (self.direction != Direction.LEFT):
                    self.direction = Direction.RIGHT
                elif (event.key == pygame.K_UP) & (self.direction != Direction.DOWN):
                    self.direction = Direction.UP
                elif (event.key == pygame.K_DOWN) & (self.direction != Direction.UP):
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head) # for every screen frame, just iteratively insert the new head
        # then we have a code snippet to pop the head in section 4 of this function
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1 # if food is eaten, then we skip the pop() method and a new section of the body is going to be
                            # inserted in the next frame refresh -> this is how the body will get longer
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # check if snake hits the boundaries
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # check if snake hits itself
        if self.head in self.snake[1:]:
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
        # for this one, we may not need to add a replay button to simplify the learning process of the agent
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        # checking the direction, continuously updating the positionings of the head
        # update to class attribute head and we will have insert() function above to add the new head
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    # game loop
    while True:
        game_over, score = game.play_step()
        if game_over == True:
            break
        
    print('Final Score', score)
        
    pygame.quit()