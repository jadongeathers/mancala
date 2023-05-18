from mancala import Mancala

class GreedyAlg():
    def __init__(self):
        super().__init__()

    def getNextGreedyMove(self, state):
        possibleActions = Mancala.generateMoves(state)

        return max([Mancala.succAndReward(state, action) for action in possibleActions], key=lambda succReward: succReward[1])

