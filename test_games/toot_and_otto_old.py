#Toot and Otto game implementation for Gamescrafters

#defines the state object for the toot and otto game
#state keeps track of 4 things:
#the player whose turn it is, the board, and both players hands
#additional methods are helper methods for the neccessary solver functions and
class State(object):
    """Base State class"""
    dash = "-"
    T = "T"
    O = "O"
    toot = T+O+O+T
    otto = O+T+T+O
    boardDimensionHeight = 4
    boardDimensionLength = 4
    diagonalConnectionsAllowed = True

    def __init__(self):
        self.firstPlayerTurn = True
        self.pieces = {}
        for x in range(State.boardDimensionLength):
            for y in range(State.boardDimensionHeight):
                self.pieces[(x,y)] = State.dash

        self.hand1 = {}
        self.hand2 = {}
        self.hand1[State.T] = 6
        self.hand1[State.O] = 6
        self.hand2[State.T] = 6
        self.hand2[State.O] = 6

    #returns a new State object that is a copy of self
    def stateCopy(self):
        copy = State()
        copy.firstPlayerTurn = self.firstPlayerTurn
        copy.pieces = self.pieces.copy()
        copy.hand1 = self.hand1.copy()
        copy.hand2 = self.hand2.copy()
        return copy

    #prints the current board with helpful indices on the left and the bottom
    def printBoard(self):
        y = State.boardDimensionHeight - 1
        while y >= 0:
            partialString = str(y) + " | "
            for x in range(State.boardDimensionLength):
                partialString += self.pieces[(x, y)] + " "
            y -= 1
            print(partialString)

        secondBottom = "    "
        for x in range(State.boardDimensionLength):
            secondBottom += "__"
        print(secondBottom)
        bottomLine = "    "
        for x in range(State.boardDimensionLength):
            bottomLine += str(x) + " "
        print(bottomLine)

    def board_is_full(self):
        for x in range(State.boardDimensionLength):
            for y in range(State.boardDimensionHeight):
                if self.pieces[(x,y)] == State.dash:
                    return False
        return True

    #returns the score dictionary for the number of words, toot and otto
    def checkForWords(self):
        score = {}
        score[State.toot] = 0
        score[State.otto] = 0
        for x in range(self.boardDimensionLength):
            for y in range(self.boardDimensionHeight):
                if self.pieces[(x,y)] != State.dash:
                    word = None
                    if self.pieces[(x,y)] == State.T:
                        word = State.toot
                    elif self.pieces[(x,y)] == State.O:
                        word = State.otto
                    if not word:
                        continue

                    if self.wordTest(x+1, y, word, 1, 0, 1):
                        score[word] += 1
                    if self.wordTest(x, y+1, word, 0, 1, 1):
                        score[word] += 1
                    if self.wordTest(x+1, y+1, word, 1, 1, 1):
                        score[word] += 1
                    if self.wordTest(x+1, y-1, word, 1, -1, 1):
                        score[word] += 1
        return score

    #helper function for checkForWords
    def wordTest(self, x, y, word, dx, dy, char_pos_in_word):
        if char_pos_in_word >= 4:
            return True
        if self.pieces.get((x,y)) != word[char_pos_in_word]:
            return False
        return self.wordTest(x+dx, y+dy, word, dx, dy, char_pos_in_word+1)


#Implementation of the neccessary functions for the solver

#assumes that player1 goes for toot and player2 goes for otto

#assumes that if the score is tied, continue playing no matter how many matches
#takes in a state parameter which is a State object
#returns a string of the options win, loss, tie, draw, unkwown
def primitive(state):
    score = state.checkForWords()
    if score[State.toot] > score[State.otto]:
        print("toot wins")
        if state.firstPlayerTurn:
            return 'win'
        return 'loss'
    elif score[State.toot] < score[State.otto]:
        print("otto wins")
        if state.firstPlayerTurn:
            return 'loss'
        return 'win'
    else:
        if state.board_is_full():
            return 'tie'
        else:
            return 'unknown'

#action is defined as a tuple with the letter, and a board location
#example of an action: ("T", (2,3))

#takes in the parameter state, a State object
#returns a list of actions that are valid to be applied to the parameter state
def gen_moves(state):
    hand = state.hand2
    if state.firstPlayerTurn:
        hand = state.hand1

    possibleActions = []
    for x in range(State.boardDimensionLength):
        y = 0
        while not state.pieces[(x,y)] == State.dash and y < State.boardDimensionHeight:
            y += 1
        if y < State.boardDimensionHeight:
            for piece in hand:
                if hand[piece]>0:
                    possibleActions.append((piece, (x,y)))
    return possibleActions

#returns the successor given by applying the parameter action to the parameter state
#the parameter action is a tuple with the letter, and a board location
#the parameter state is a State object
#must pass in a valid state and a valid action for that state, does not check
def do_move(state, action):
    successor = state.stateCopy()
    piece, loc = action

    successor.firstPlayerTurn = not state.firstPlayerTurn
    successor.pieces[(loc)] = piece
    if state.firstPlayerTurn:
        successor.hand1[piece] -= 1
    else:
        successor.hand2[piece] -= 1
    return successor

init_pos = State()




#helpful prints for reference, understanding the code, and debugging
"""
def example():
    print 'the initial position is the following:'
    init_pos.printBoard()
    print 'hand1=' + str(init_pos.hand1)
    print 'hand2=' + str(init_pos.hand2)
    print 'firstPlayerTurn=' + str(init_pos.firstPlayerTurn)
    possibleActions = gen_moves(init_pos)
    print 'these are the possible actions:'
    print possibleActions
    print 'primitive value:'
    print primitive(init_pos)
    s = make_move(init_pos, possibleActions[6])
    print 'this is the state after a move has been made'
    s.printBoard()
    print 'hand1=' + str(s.hand1)
    print 'hand2=' + str(s.hand2)
    print 'firstPlayerTurn=' + str(s.firstPlayerTurn)
    possibleActions = gen_moves(s)
    print 'New possible actions:'
    print possibleActions
    print 'primitive value:'
    print primitive(s)
"""