import pickle
import random
from collections import defaultdict
from mancala import Mancala
from tqdm import tqdm


class QAgent(Mancala):
    def __init__(self, lr=0.1, discount=1.0, epsilon=1.0):
        super().__init__()
        self.lr = lr
        self.discount = discount
        self.epsilon = epsilon
        self.qValues = defaultdict(lambda: defaultdict(float))

    def decayEpsilon(self):
        self.epsilon *= 0.99

    def stateToTuple(self, state):
        return tuple(state[0]), state[1]

    def update(self, state, action):
        nextState, reward = self.succAndReward(state, action)
        state = self.stateToTuple(state)
        nextState = self.stateToTuple(nextState)
        bestValue = max(self.qValues[nextState]) if nextState in self.qValues else 0
        tempDiff = reward + self.discount * bestValue - self.qValues[state][action]
        self.qValues[state][action] += self.lr * tempDiff

    def getNextMove(self, state):
        # with probability epsilon return a random action to explore the environment
        if random.random() < self.epsilon:
            return random.choice(self.generateMoves(state))

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            if self.stateToTuple(state) not in self.qValues:
                return random.choice(self.generateMoves(state))

            state = self.stateToTuple(state)
            bestValue = max(self.qValues[state])
            bestActions = [i for i, val in enumerate(self.qValues[state]) if val == bestValue]
            return random.choice(bestActions)


if __name__ == '__main__':
    # Create a Q-learning agent
    agent = QAgent()

    # Train the agent
    num_episodes = 10000
    for episode in tqdm(range(num_episodes)):
        mancala = Mancala()
        train_state = mancala.startState()
        while not mancala.isEnd(train_state):
            # Choose an action using the epsilon-greedy strategy
            train_action = agent.getNextMove(train_state)

            # Execute the action and observe the next state and reward
            train_nextState, reward = mancala.succAndReward(train_state, train_action)

            # Update the Q-values table
            agent.update(train_state, train_action)

            # Transition to the next state
            train_state = train_nextState

        # Decay the exploration rate after each episode
        agent.decayEpsilon()

    # Save the learned Q-values table for later use, if desired
    q_values_table = agent.qValues
    with open('qValues.pkl', 'wb') as f:
        pickle.dump(q_values_table, f)
