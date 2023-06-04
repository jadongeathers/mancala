import argparse
import random
import time
import tkinter as tk
import copy
#from algorithms import *
from tqdm import tqdm


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
        state = copy.deepcopy(state)
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

        if player == 1 and currDropIndex == 13:
            currDropIndex = 0
        if player == 2 and currDropIndex == 6:
            currDropIndex = 7
        if player == 2 and currDropIndex == 14:
            currDropIndex = 0

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
            if currDropIndex > 6 and state[0][currDropIndex] == 0 and state[0][12 - currDropIndex] != 0:
                state[0][13] += 1 + state[0][(12 - currDropIndex)]
                state[0][(12 - currDropIndex)] = 0
            else:
                state[0][currDropIndex] += 1

            if self.isEnd(state):
                return returnEndState(player)
            else:
                return ([state[0], 1], state[0][13] - origBankScore)

        # if currDropIndex > 12:
        #     currDropIndex = 0
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

    def getGameInfo(self, gameplay):
        agent1 = None
        agent2 = None

        # Agent 1 selection
        agentNum = int(input('Select agent 1:\n[1]\tRandom Algorithm\n[2]\tGreedy Algorithm\n[3]\tMinimax Algorithm\nYour selection: '))
        if agentNum not in [1, 2, 3]:
            agentNum = input('Invalid input. Select an agent type:\n[1]\tRandom Algorithm'
                             '\n[2]\tGreedy Algorithm\n[3]\tMinimax Algorithm\nYour selection: ')
        if agentNum == 1:
            agent1 = RandomAlg()
        if agentNum == 2:
            agent1 = GreedyAlg()
        if agentNum == 3:
            agent1 = MinimaxAlphaBetaAlg()

        if gameplay != 'human-computer':
            # Agent 2 selection
            agentNum = int(input('Select agent 2:\n[1]\tRandom Algorithm\n[2]\tGreedy Algorithm\n[3]\tMinimax Algorithm\nYour selection: '))
            if agentNum not in [1, 2, 3]:
                agentNum = input('Invalid input. Select an agent type:\n[1]\tRandom Algorithm'
                                 '\n[2]\tGreedy Algorithm\n[3]\tMinimax Algorithm\nYour selection: ')
            if agentNum == 1:
                agent2 = RandomAlg()
            if agentNum == 2:
                agent2 = GreedyAlg()
            if agentNum == 3:
                agent2 = MinimaxAlphaBetaAlg()

        nGames = int(input('Specify the number of games: '))
        return agent1, agent2, nGames

    def playGame(self, gameplay, verbose=False):
        if gameplay == 'human-human' or gameplay == 'human-computer':
            game = MancalaDisplay(gameplay=gameplay)
            game.playGame(gameplay, verbose=verbose)

        elif gameplay == 'computer-computer':
            agent1, agent2, nGames = self.getGameInfo(gameplay)
            gameResults = {}

            for i in tqdm(range(nGames)):

                state = self.startState()
                while not self.isEnd(state):
                    # Agent 1 makes a move
                    if state[1] == 1:
                        action = agent1.getNextMove(state)
                        state, reward = self.succAndReward(state, action)
                    else:
                        action = agent2.getNextMove(state)
                        state, reward = self.succAndReward(state, action)

                winner, agent1Score, agent2Score = self.getWinner(state, verbose)
                results = {'winner': winner, 'player1Score': agent1Score, 'player2Score': agent2Score}
                gameResults[i] = results

            self.reportGameStats(gameResults)

        else:
            print('Please specify a valid gameplay using --gameplay')

    def reportGameStats(self, gameResults):
        numAgent1Wins = sum([1 for key in gameResults if gameResults[key]['winner'] == 'Player 1 wins!'])
        numAgent2Wins = sum([1 for key in gameResults if gameResults[key]['winner'] == 'Player 2 wins!'])
        numTies = sum([1 for key in gameResults if gameResults[key]['winner'] == "It's a tie!"])
        totalGames = numAgent1Wins + numAgent2Wins + numTies
        agent1WinRate = numAgent1Wins / totalGames
        agent2WinRate = numAgent2Wins / totalGames
        tieRate = numTies / totalGames
        print('\n')
        print('===== GAME STATISTICS =====')
        print(f'Player 1 win rate:\t {agent1WinRate} ({numAgent1Wins} / {totalGames})')
        print(f'Player 2 win rate:\t {agent2WinRate} ({numAgent2Wins} / {totalGames})')
        print(f'Tie rate:\t\t {tieRate} ({numTies} / {totalGames})')
        print('\n')

    def getWinner(self, state, verbose):
        sumPlayerOne = state[0][6]
        sumPlayerTwo = state[0][13]
        if sumPlayerOne > sumPlayerTwo:
            winner = 'Player 1 wins!'
        elif sumPlayerTwo > sumPlayerOne:
            winner = 'Player 2 wins!'
        else:
            winner = "It's a tie!"
        if verbose:
            print(winner)
            print('Final scores:')
            print('Player 1: ', sumPlayerOne)
            print('Player 2: ', sumPlayerTwo)
        return winner, sumPlayerOne, sumPlayerTwo


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
        self.clickedPocket = tk.IntVar()

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
                self.clickedPocket.set(i if i < 6 else i + 1)
                action = i if i < 6 else i + 1
                if action in self.generateMoves(self.currentState):
                    self.makeMove(action)
                    #self.makeHumanMove()
                break
        #self.makeHumanMove()

    def makeMove(self, action):
        prevState = self.currentState
        state, reward = self.succAndReward(self.currentState, action)
        self.displayState(state)
        self.currentState = state
        if self.isEnd(state):
            self.showWinner()
            return
        print(f"Player {state[1]}'s turn")

    def showWinner(self):
        sumPlayerOne = self.currentState[0][6]
        sumPlayerTwo = self.currentState[0][13]
        if sumPlayerOne > sumPlayerTwo:
            winner = 'Player 1 wins!'
        elif sumPlayerTwo > sumPlayerOne:
            winner = 'Player 2 wins!'
        else:
            winner = "It's a tie!"
        self.canvas.create_text(200, 350, text=winner, font=('Arial', 20), fill='red')
        self.root.after(5000, self.root.quit)

    def makeHumanMove(self):
        print('Making human move')
        self.root.wait_variable(self.clickedPocket)
        self.clickedPocket = tk.IntVar()

    def makeComputerMove(self, agent):
        print('Making computer move')
        action = agent.getNextMove(self.currentState)
        self.makeMove(action)

    def playGame(self, gameplay, verbose=False):
        if gameplay == 'human-human':
            print("Player 1's turn")
            self.displayState(self.currentState)
            self.root.mainloop()

        elif gameplay == 'human-computer':
            agent, _, nGames = self.getGameInfo(gameplay)
            players = ['human', 'computer']
            firstPlayer = random.choice(players)


            secondPlayer = list(set(players) - {firstPlayer})[0]
            #secondPlayer = ''

            if firstPlayer == 'human':
                print('You go first.')
                secondPlayer = 'computer'
            else:
                print('The computer goes first.')
                secondPlayer = 'human'

            gameResults = {}
            for i in range(nGames):
                self.currentState = self.startState()
                self.displayState(self.currentState)
                print("Player 1's turn")

                while not self.isEnd(self.currentState):
                    # Player 1 makes a move
                    if self.currentState[1] == 1:
                        if firstPlayer == 'human':
                            self.makeHumanMove()
                        else:
                            self.makeComputerMove(agent)

                    # Player 2 makes a move
                    else:
                        if secondPlayer == 'human':
                            self.makeHumanMove()
                        else:
                            self.makeComputerMove(agent)

                winner, player1Score, player2Score = self.getWinner(self.currentState, verbose)
                self.showWinner()
                results = {'winner': winner, 'player1Score': player1Score, 'player2Score': player2Score}
                gameResults[i] = results

            self.reportGameStats(gameResults)

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


class MinimaxAlphaBetaAlg(Mancala):
    def __init__(self):
        super().__init__()
        self.depth = 2

    def evaluationFunction(self, state):
        # Evaluation will be difference in p1 score vs p2
        player = state[1]
        if player == 1:
            return state[0][6] - state[0][13]
        else:
            return state[0][13] - state[0][6]

    def endScore(self, state):
        player = state[1]
        winReward = 100
        diff = 0
        if player == 1:
            diff = state[0][6] - state[0][13]
        else:
            diff = state[0][13] - state[0][6]

        if diff > 0:
            return winReward + diff
        elif diff < 0:
            return -winReward + diff
        else:
            return 0

    def getNextMove(self, state):

        def findBestAction(state, depth, currPlayer, maxPlayer, alpha, beta):
            if self.isEnd(state):
                return self.endScore(state)
            if depth == 0:
                return self.evaluationFunction(state)

            if currPlayer == maxPlayer:
                # Max player layer, want max over min player actions
                valuePlusAction = None
                for potentialAction in self.generateMoves(state):
                    if valuePlusAction is None:
                        if currPlayer == 1:
                            valuePlusAction = (
                            findBestAction(self.succAndReward(state, potentialAction)[0], depth,
                                                2, maxPlayer, alpha, beta), potentialAction)
                        else:
                            valuePlusAction = (
                                findBestAction(self.succAndReward(state, potentialAction)[0], depth,
                                               1, maxPlayer, alpha, beta), potentialAction)
                    else:
                        potentialValuePlusAction = None
                        if currPlayer == 1:
                            potentialValuePlusAction = (
                            findBestAction(self.succAndReward(state, potentialAction)[0], depth,
                                                2, maxPlayer, alpha, beta), potentialAction)
                        else:
                            potentialValuePlusAction = (
                                findBestAction(self.succAndReward(state, potentialAction)[0], depth,
                                               1, maxPlayer, alpha, beta), potentialAction)

                        valuePlusAction = max(valuePlusAction, potentialValuePlusAction)

                    if beta is not None and valuePlusAction[0] > beta:
                        break

                    if alpha is None:
                        alpha = valuePlusAction[0]
                    else:
                        alpha = max(alpha, valuePlusAction[0])

                if depth == self.depth:
                    #print(valuePlusAction[0])
                    return valuePlusAction[1]
                else:
                    return valuePlusAction[0]

            else:
                valuePlusAction = None
                for potentialAction in self.generateMoves(state):
                    if valuePlusAction is None:
                        if currPlayer == 1:
                            valuePlusAction = (
                            findBestAction(self.succAndReward(state, potentialAction)[0], depth - 1,
                                                2, maxPlayer, alpha, beta), potentialAction)
                        else:
                            valuePlusAction = (
                                findBestAction(self.succAndReward(state, potentialAction)[0], depth - 1,
                                               1, maxPlayer, alpha, beta), potentialAction)
                    else:
                        potentialValuePlusAction = None
                        if currPlayer == 1:
                            potentialValuePlusAction = (
                            findBestAction(self.succAndReward(state, potentialAction)[0], depth - 1,
                                                2, maxPlayer, alpha, beta), potentialAction)
                        else:
                            potentialValuePlusAction = (
                                findBestAction(self.succAndReward(state, potentialAction)[0], depth - 1,
                                               1, maxPlayer, alpha, beta), potentialAction)

                        valuePlusAction = min(valuePlusAction, potentialValuePlusAction)

                    if alpha is not None and valuePlusAction[0] < alpha:
                        break

                    if beta is None:
                        beta = valuePlusAction[0]
                    else:
                        beta = min(beta, valuePlusAction[0])

                return valuePlusAction[0]


        maxPlayer = state[1]
        return findBestAction(state, self.depth, maxPlayer, maxPlayer, None, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gameplay', choices=['human-human', 'human-computer', 'computer-computer'],
                        default='human-computer',
                        help='The mode of gameplay')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    mancala = Mancala()
    mancala.playGame(args.gameplay, args.verbose)


