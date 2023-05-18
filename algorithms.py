import random
from mancala import Mancala


class RandomAlg(Mancala):
    def __init__(self):
        super().__init__()

    def getNextMove(self, state):
        possibleActions = self.generateMoves(state)
        action = random.choice(possibleActions)
        return action


class GreedyAlg(Mancala):
    def __init__(self):
        super().__init__()

    def getNextMove(self, state):
        possibleActions = self.generateMoves(state)
        rewards = [self.succAndReward(state, action)[1] for action in possibleActions]
        bestIndices = [i for i in range(len(possibleActions)) if rewards[i] == max(rewards)]
        actionIndex = random.choice(bestIndices)
        action = possibleActions[actionIndex]
        return action

