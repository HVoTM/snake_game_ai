# reward
- eat food: +10
- game over: -10
- else: 0

# action
[1, 0, 0] -> straight
[0, 1, 0] -> right turn
[0, 0, 1] -> left turn

# state
tells our snake about some information about the game right now 
- 11 values
[danger straight, danger right, danger left,

direction left, direction right, 
direction up, direction down,

food left, food right,
food up, food down]

# (Deep) Q Learning

__Q value__ = quality of action
0. Init Q value(= init model)
1. Choose action (model.predict(state)) or random move
2. Perform action
3. Measure reward
4. Update Q value (+ train model) -> Repeat

## Bellman Equation:
$$NewQ(s, a) = Q(s,a) + \alpha[R(s, a) + \gamma maxQ'(s',a')-Q(s,a) ]$$

## Q update rule simplified
* Q = model.predict(state_0)
* Q_new = R + gamma * max(Q(state_1))

## Loss function
$loss =(Q_{new}-Q)^2$
