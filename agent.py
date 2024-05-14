import torch
import random
import numpy as np
from snake_game import SnakeGame, Direction, Point
from collections import deque ; "https://docs.python.org/3/library/collections.html#deque-objects"
from typing import List
from model import Linear_QNet, QTrainer
from helper import plot

# define parameters as constants, can change to configure the settings of the agent
MAX_MEMORY= 100_000
BATCH_SIZE = 1000
LR = 0.001 # (LR: learning rate)

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate (0 < n <= 1) - can play around
        self.memory = deque(maxlen=MAX_MEMORY) # if exceeds the max capacity, the deque object will popleft()
        # deque is a pretty useful data structures to implement in Python due to its complexity and easy for modification
        self.model = Linear_QNet(11, 256, 3) # input: 11, output: 3, middle layer: customizable
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # TODO: model trainer
        
    def get_state(self, game):
        head = game.snake[0]
        # Create four points indicating the adjacent blocks in each direction
        # We will be using this detect danger ahead of that direction
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        # check if the current frame's direction is which of the below values
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # array map of 11 states for the game to learn
        """ 
        [danger straight, danger right, danger left,

        direction left, direction right, 
        direction up, direction down,

        food left, food right,
        food up, food down]
        """
        state = [
            # Danger straight
            (dir_r and game._is_collision(point_r)) or # example: agent is moving to the right and check if the next right block 
            (dir_l and game._is_collision(point_l)) or # (point_r) will be setting is_collision() to true
            (dir_u and game._is_collision(point_u)) or 
            (dir_d and game._is_collision(point_d)),

            # Danger right
            (dir_u and game._is_collision(point_r)) or # same as going to the right, looking down, which is to the right of 
            (dir_d and game._is_collision(point_l)) or # the direction the snake is going and check if there will be a collision
            (dir_l and game._is_collision(point_u)) or 
            (dir_r and game._is_collision(point_d)),

            # Danger left
            (dir_d and game._is_collision(point_r)) or # same as above, snake is currently going right, check the block going up 
            (dir_u and game._is_collision(point_l)) or # which is to the left of the current direction and check collision
            (dir_r and game._is_collision(point_u)) or 
            (dir_l and game._is_collision(point_d)),
            
            # Move direction
            dir_l, # only one is true
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int) # setting to int will cast on boolean to 0/1
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action ,reward, next_state, done)) # will popleft if reach max_memory
                        # we store this as tuple since we will be sampling each state distinctively
                        # also not to mess up when sampling in long-memory training 

    def train_long_memory(self): # grab a maximum of batch_size of memory to do long-term training
        # first off, check if a batch size is too large for learning
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # this will generate a list of tuples
        else:
            mini_sample = self.memory
        
        # * for unpacking each element in the tuples, then zip all the values of 
        # an element and return as one of the results
        """Similar code:
        for state, action, reward, next_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, next_state, done)
        """
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        # random moves: tradeoff exploration/exploitation
        self.epsilon = 80 - self.n_games # hardcoded the 80 decrementing, the more we play -> less random the game is
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon: # randomly set to a random move if smaller than epsilon
            move = random.randint(0, 2)
            final_move[move] = 1 # set to left/straight/right move
        else: # else we will do predictions 
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # make prediction
            move = torch.argmax(prediction).item() # take the argmax of the tensor, retrieve the item since we are still having a tensor
            final_move[move] = 1

        return final_move
    
def train():
    # score stats to keep track of as well as usage for display
    plot_scores = [] # TODO: try with plot_scores = List[float]
    plot_mean_scores = [] # also check if numpy values also apply
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        # get the old state
        prev_state = agent.get_state(game)
        
        # get move based on the current state
        latest_move = agent.get_action(state=prev_state)
        
        # perform the move and record the new state
        reward, done, score = game.play_step(latest_move)
        new_state = agent.get_state(game)
        
        # train short memory
        agent.train_short_memory(prev_state, latest_move, reward, new_state, done)
        
        # remember
        agent.remember(prev_state, latest_move, reward, new_state, done)
        
        if done:
            game.newgame()
            agent.n_games += 1
             # train long memory: replay the agent's previous experience
            # and train all the previous moves and games played -> help improvements
            agent.train_long_memory()
            
            if score > record:
                record = score
                # TODO: record high score: 
                agent.model.save()
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record) 
            
            # TODO: plot the stats on graph      
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()