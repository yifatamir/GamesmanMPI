WIN, LOSS, TIE, DRAW, UNDECIDED = "WIN", "LOSS", "TIE", "DRAW", "UNDECIDED"

WIDTH = 3
HEIGHT = 3

BORDER = 'B'
X = 'X'
O = 'O'
BLANK = '_'

def initial_position():
    return BLANK * WIDTH * HEIGHT

def toLoc(i):
    x = i % WIDTH
    y = i // WIDTH
    return (x, y)

def toIndex(loc):
    x, y = loc
    return x + (y * WIDTH)

def findSpaces(pos):
    for i, p in enumerate(pos):
        if p == BLANK:
            yield i

def findNonSpaces(pos):
    for i, p in enumerate(pos):
        if p != BLANK:
            yield i

def getPiece(pos, x, y):
    if x < 0 or x > 2 or y < 0 or y > 2:
        return 'B'
    else:
        return pos[toIndex((x, y))]

def getPlayer(pos):
    if pos.count(O) >= pos.count(X):
        return X
    else:
        return O

def primitive(pos):
    '''
    >>> primitive(BLANK * 9)
    'undecided'
    >>> primitive(X * 9)
    'lose'
    >>> primitive(X + X + O +
    ...           O + O + X +
    ...           X + O + X)
    'tie'
    >>> primitive(X + X + X +
    ...           O + O + X +
    ...           X + O + O)
    'lose'
    >>> primitive(O + X + X +
    ...           O + O + X +
    ...           X + O + X)
    'lose'
    >>> primitive(X + O + O +
    ...           O + X + X +
    ...           X + O + X)
    'lose'
    >>> primitive(O + O + X +
    ...           O + X + X +
    ...           X + X + O)
    'lose'
    '''
    for x, y in [toLoc(i) for i in
                 findNonSpaces(pos)]:
        piece = getPiece(pos, x, y)
        if ((getPiece(pos, x + 1, y) == piece and
             getPiece(pos, x + 2, y) == piece) or
            (getPiece(pos, x, y + 1) == piece and
             getPiece(pos, x, y + 2) == piece) or
            (getPiece(pos, x + 1, y + 1) == piece and
             getPiece(pos, x + 2, y + 2) == piece) or
            (getPiece(pos, x - 1, y + 1) == piece and
             getPiece(pos, x - 2, y + 2) == piece)):
            return LOSS
    if BLANK in pos:
        return UNDECIDED
    else:
        return TIE

def gen_moves(pos):
    '''
    >>> len(generateMoves('_' * 9))
    9
    >>> generateMoves('_' * 9)[:3]
    [(0, 0), (1, 0), (2, 0)]
    >>> generateMoves('_' * 9)[3:6]
    [(0, 1), (1, 1), (2, 1)]
    >>> generateMoves('_' * 9)[6:]
    [(0, 2), (1, 2), (2, 2)]
    >>> generateMoves('XOX'
    ...               'OXO'
    ...               'X__')
    [(1, 2), (2, 2)]
    '''
    return [toLoc(i) for i in findSpaces(pos)]

def do_move(position, move):
    '''
    >>> doMove('_', (0, 0))
    'X'
    >>> doMove('X_O', (1, 0))
    'XXO'
    >>> doMove('XOX'
    ...        'OXO'
    ...        'X__', (1, 2))
    'XOXOXOXO_'
    >>> doMove('XOX'
    ...        'OXO'
    ...        'X__', (2, 2))
    'XOXOXOX_O'
    >>> doMove('XOX'
    ...        'OXO'
    ...        '___', (0, 2))
    'XOXOXOX__'
    '''
    player = getPlayer(position)
    index = toIndex(move)
    return position[:index] + player + position[index + 1:]
