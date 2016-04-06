
WIN, LOSS, TIE, DRAW, UNDECIDED = 0, 1, 2, 3, 4
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py

# Used for logging/display purposes
STATE_MAP       = {0:"win", 1:"loss", 2:"tie", 3:"draw", 4:"undecided"}
JOB_TYPE_MAP   = {0:"finished", 1:"lookup", 2:"resolve", 3:"send back", 4:"distribute", 5:"check for updates"}

def negate(state):
    neg = (1, 0, 2, 3, 4)
    return neg[state]

def to_str(state):
    str_rep = ("WIN", "LOSS", "TIE", "DRAW", "UNDECIDED")
    return str_rep[state]
