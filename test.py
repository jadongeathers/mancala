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
    # print(mancala.succAndReward(startState, 2))

    # endState = [[0, 0, 0, 0, 0, 0, 10,
    #             2, 2, 2, 2, 2, 2, 0], 2]
    #print(mancala.succAndReward(endState, 7))

    #captureState = [[1, 0, 2, 3, 0, 0, 10,
                    #2, 2, 2, 2, 2, 2, 0], 1]
    #print(mancala.succAndReward(captureState, 0))

    #wrapAroundState = [[1, 0, 2, 3, 0, 13, 10,
                       # 2, 2, 2, 2, 2, 12, 0], 2]
    #print(mancala.succAndReward(wrapAroundState, 12))

    def testCaptureWrapAround():
        state = [[
            0, 1, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 8, 0
        ], 1]
        result = [[
            0, 1, 0, 0, 0, 0, 11, 2, 1, 1, 1, 1, 0, 0
        ], 2]
        test = mancala.succAndReward(state, 5)
        if test != result:
            print('Started with: ', state)
            print('Expected: ', result)
            print('Got: ', test)
            return
        print('testCaptureWrapAround passed!')

    testCaptureWrapAround()




if __name__ == '__main__':
    main()