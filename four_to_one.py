#################################################
# 4 - 1 Portion
#################################################

LOSS, WIN, TIE, DRAW, UNDECIDED = "LOSS", "WIN", "TIE", "DRAW", "UNDECIDED"

initial_position = 5

def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]

def do_move(x, move):
    return x + move

def primitive(x):
    if x <= 0:
        return LOSS
    else:
        return UNDECIDED
