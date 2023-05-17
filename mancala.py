class Mancala:
    def __init__(self):
        self.piecesPerPocket = 4
        self.numPockets = 12
        self.numBanks = 2
        self.numPlayers = 2

    def startState(self):
        # 15-list of the format [[P1_pockets, B1, P2_pockets, B2], player]
        return [[4, 4, 4, 4, 4, 4, 0,
                 4, 4, 4, 4, 4, 4, 0],
                 1]

    def actions(self):
        # Select a pocket, using index in state list
        return [i for i in range(13) if i != 6]

    def generateMoves(self, state):
        # Find non-empty pockets
        player = state[1]
        if player == 1:
            return [i for i in range(0, 6) if state[0][i] > 0]
        else:
            return [i for i in range(7, 13) if state[0][i] > 0]

    def succAndReward(self, state, action):
        # Assumes action is a valid move

        # If no more pieces are on your side, the other player captures
        # everything on their side
        player = state[1]
        if self.isEnd(state):
            sumOne = 0
            sumTwo = 0
            for i in range(6):
                sumOne += state[0][i]
                sumTwo += state[0][7 + i]

            if player == 1:
                return ([[0, 0, 0, 0, 0, 0, state[0][6] + sumOne,
                        0, 0, 0, 0, 0, 0, state[0][13] + sumTwo],
                        player], state[0][6] + sumOne - state[0][13] - sumTwo)
            else:
                return ([[0, 0, 0, 0, 0, 0, state[0][6] + sumOne,
                          0, 0, 0, 0, 0, 0, state[0][13] + sumTwo],
                         player], state[0][13] + sumTwo - state[0][6] - sumOne)


        # In all cases, we drop a piece in each newly visited pocket
        origBankScore = 0
        if player == 1:
            origBankScore = state[0][6]
        else:
            origBankScore = state[0][13]

        numStones = state[0][action]
        state[0][action] = 0
        currDropIndex = action + 1
        while numStones > 1:
            if currDropIndex == 6:
                if player == 2:
                    currDropIndex += 1

            if currDropIndex > 12:
                if player == 1:
                    currDropIndex = 0
                elif currDropIndex > 13:
                    currDropIndex = 0

            state[0][currDropIndex] += 1
            numStones -= 1
            currDropIndex += 1

        # If the last piece lands in the bank, we go again
        if player == 1 and currDropIndex == 6:
            state[0][currDropIndex] += 1

            return (state, state[0][6] - origBankScore)
        elif player == 2 and currDropIndex == 13:
            state[0][currDropIndex] += 1

            return (state, state[0][13] - origBankScore)

        # If the last piece lands on your side in an empty tray,
        # win the pieces in that pocket and the opponent's adjacent
        # pocket
        if player == 1 and currDropIndex < 6:
            if state[0][currDropIndex] == 0:
                state[0][6] += 1 + state[0][(12 - currDropIndex)]
                state[0][(12 - currDropIndex)] = 0
            else:
                state[0][currDropIndex] += 1

            return ([state[0], 2], state[0][6] - origBankScore)

        if player == 2 and currDropIndex < 13:
            if state[0][currDropIndex] == 0:
                state[0][13] += 1 + state[0][(12 - currDropIndex)]
                state[0][(12 - currDropIndex)] = 0
            else:
                state[0][currDropIndex] += 1

            return ([state[0], 1], state[0][13] - origBankScore)

        if currDropIndex > 12:
                currDropIndex = 0
        state[0][currDropIndex] += 1
        if player == 1:
            return ([state[0], 2], state[0][6] - origBankScore)
        else:
            return ([state[0], 1], state[0][13] - origBankScore)


    def isEnd(self, state):
        # If our side is empty or the other side is empty, True
        stonesLeftOne = 0
        stonesLeftTwo = 0
        for i in range(6):
            stonesLeftOne += state[0][i]
            stonesLeftTwo += state[0][7 + i]

        return stonesLeftOne == 0 or stonesLeftTwo == 0

