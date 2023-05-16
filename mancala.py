class Mancala:
    def __init__(self):
        self.piecesPerPocket = 4
        self.numPockets = 12
        self.numBanks = 2
        self.numPlayers = 2

    def startState(self):
        # 15-list of the format [[pockets], [banks], player]
        pass

    def actions(self):
        # Select a pocket
        pass

    def generateMoves(self):
        # Find non-empty pockets
        pass

    def succAndReward(self):
        # If no more pieces are on your side, the other player captures
        # everything on their side

        # In all cases, we drop a piece in each newly visited pocket
        # If the last piece lands in the bank, we go again

        # If the last piece lands on your side in an empty tray,
        # win the pieces in that pocket and the opponent's adjacent
        # pocket
        pass

    def isEnd(self):
        # If our side is empty or the other side is empty, True
        pass

