from mancala import Mancala


def main():
    mancala = Mancala()

    startState = mancala.startState()
    """
    print(startState)
    print(mancala.actions())
    print(mancala.generateMoves(startState))
    startState[1] = 2
    print(mancala.generateMoves(startState))
    """
    #startState[1] = 2
    #print(mancala.succAndReward(startState, 2))

    # endState = [[0, 0, 0, 0, 0, 0, 10,
    #             2, 2, 2, 2, 2, 2, 0], 2]
    #print(mancala.succAndReward(endState, 7))

    #captureState = [[1, 0, 2, 3, 0, 0, 10,
                    #2, 2, 2, 2, 2, 2, 0], 1]
    #print(mancala.succAndReward(captureState, 0))

    #wrapAroundState = [[1, 0, 2, 3, 0, 13, 10,
                       # 2, 2, 2, 2, 2, 12, 0], 2]
    #print(mancala.succAndReward(wrapAroundState, 12))

    fullWrapAroundStatePlusCapture = [[2, 2, 2, 2, 2, 2, 0,
     0, 0, 0, 0, 0, 13, 0], 2]
    print(mancala.succAndReward(fullWrapAroundStatePlusCapture, 12))

    # captureState = [[1, 0, 2, 3, 0, 0, 10,
    # 2, 2, 2, 2, 2, 2, 0], 1]
    # print(mancala.succAndReward(captureState, 0))

    # Also make sure to test capturing all the way back around to og pocket



if __name__ == '__main__':
    main()