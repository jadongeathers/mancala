import tkinter as tk

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
        def returnEndState(player):
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
            if self.isEnd(state):
                return returnEndState(player)
            else:
                return (state, state[0][6] - origBankScore)
        elif player == 2 and currDropIndex == 13:
            state[0][currDropIndex] += 1
            if self.isEnd(state):
                return returnEndState(player)
            else:
                return (state, state[0][13] - origBankScore)

        # If the last piece lands on your side in an empty tray,
        # win the pieces in that pocket and the opponent's adjacent
        # pocket
        if player == 1 and currDropIndex < 6:
            if state[0][currDropIndex] == 0 and state[0][12 - currDropIndex] != 0:
                state[0][6] += 1 + state[0][(12 - currDropIndex)]
                state[0][(12 - currDropIndex)] = 0
            else:
                state[0][currDropIndex] += 1
            if self.isEnd(state):
                return returnEndState(player)
            else:
                return ([state[0], 2], state[0][6] - origBankScore)

        if player == 2 and currDropIndex < 13:
            if state[0][currDropIndex] == 0 and state[0][12 - currDropIndex] != 0:
                state[0][13] += 1 + state[0][(12 - currDropIndex)]
                state[0][(12 - currDropIndex)] = 0
            else:
                state[0][currDropIndex] += 1

            if self.isEnd(state):
                return returnEndState(player)
            else:
                return ([state[0], 1], state[0][13] - origBankScore)

        if currDropIndex > 12:
            currDropIndex = 0
        state[0][currDropIndex] += 1
        if player == 1:
            if self.isEnd(state):
                return returnEndState(player)
            else:
                return ([state[0], 2], state[0][6] - origBankScore)
        else:
            if self.isEnd(state):
                return returnEndState(player)
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

    def playGame(self, gameplay):
        if gameplay == 'human-human' or gameplay == 'human-computer':
            game = MancalaDisplay(gameplay=gameplay)
            game.playGame()
            return # How do we exit the game loop?
            # TODO: randomize who is the player and who is the computer

class MancalaDisplay(Mancala):
    def __init__(self, gameplay):
        super().__init__()
        self.root = tk.Tk()
        self.root.title('Mancala')
        self.canvas = tk.Canvas(self.root, width=400, height=700)
        self.canvas.pack()
        self.gameplay = gameplay

        self.board = self.canvas.create_rectangle(50, 10, 350, 690, outline='black', width=2)
        self.pockets = []
        self.banks = []

        self.currentState = self.startState()

        # Pockets for player 1 (indices 0-5)
        for i in range(6):
            x = 120
            y = 130 + 88 * i
            pocket = self.canvas.create_oval(x - 37.5, y - 37.5, x + 37.5, y + 37.5, fill='white', outline='black', width=2)
            self.pockets.append(pocket)

        # Pockets for player 2 (indices 7-12)
        for i in range(6):
            x = 280
            y = 570 - 88 * i
            pocket = self.canvas.create_oval(x - 37.5, y - 37.5, x + 37.5, y + 37.5, fill='white', outline='black', width=2)
            self.pockets.append(pocket)

        # Player banks
        x = 200
        y = 650
        bank1 = self.canvas.create_rectangle(x - 115, y - 30, x + 115, y + 30, fill='white', outline='black', width=2)
        self.banks.append(bank1)

        x = 200
        y = 50
        bank2 = self.canvas.create_rectangle(x - 115, y - 30, x + 115, y + 30, fill='white', outline='black', width=2)
        self.banks.append(bank2)

        self.canvas.bind("<Button-1>", self.handleClick)

    def displayState(self, state):
        pocket_counts = []
        for i in range(13):
            if i != 6:
                count = state[0][i]
                pocket_counts.append(count)

        bank_counts = []
        for i in range(2):
            count = state[0][(i + 1) * 7 - 1]
            bank_counts.append(count)

        # Clear existing count labels
        self.canvas.delete('pocket_count')
        self.canvas.delete('bank_count')

        for i, pocket in enumerate(self.pockets):
            coords = self.canvas.coords(pocket)
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            self.canvas.create_text(x, y, text=str(pocket_counts[i]), tags='pocket_count')

        for i, bank in enumerate(self.banks):
            coords = self.canvas.coords(bank)
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            self.canvas.create_text(x, y, text=str(bank_counts[i]), tags='bank_count')

    def handleClick(self, event):
        x, y = event.x, event.y
        for i, pocket in enumerate(self.pockets):
            bbox = self.canvas.bbox(pocket)
            if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                action = i if i < 6 else i + 1
                if action in self.generateMoves(self.currentState):
                    self.makeMove(action)
                break

    def makeMove(self, action):
        print('current: ', self.currentState)
        state, reward = self.succAndReward(self.currentState, action)
        print('new: ', state)
        self.displayState(state)
        print('Reward: ', reward)
        self.currentState = state
        if self.isEnd(state):
            #state, reward = self.succAndReward(self.currentState, action)
            #self.displayState(state)
            #print('Reward: ', reward)
            self.showWinner()
            return
        print(f"Player {state[1]}'s turn")

    def showWinner(self):
        #sumPlayerOne = sum(self.currentState[0][:6])
        sumPlayerOne = self.currentState[0][6]
        #sumPlayerTwo = sum(self.currentState[0][7:13])
        sumPlayerTwo = self.currentState[0][13]
        if sumPlayerOne > sumPlayerTwo:
            winner = 'Player 1 wins!'
        elif sumPlayerTwo > sumPlayerOne:
            winner = 'Player 2 wins!'
        else:
            winner = "It's a tie!"
        self.canvas.create_text(200, 350, text=winner, font=('Arial', 20), fill='red')

    def playGame(self):
        print("Player 1's turn")
        self.displayState(self.currentState)
        self.root.mainloop()


if __name__ == '__main__':
    mancala = Mancala()
    mancala.playGame('human-human')


