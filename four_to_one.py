#################################################
# 4 - 1 Portion
#################################################

LOSS, WIN, TIE, DRAW = "LOSS", "WIN", "TIE", "DRAW"

initial_position = 4

def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]

def do_move(x, move):
    return x + move

def primitive(x):
    if x <= 0:
        return LOSS
