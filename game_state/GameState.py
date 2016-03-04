from mpi4py import MPI
import hashlib
import sys

WIN, LOSS, TIE, DRAW = "WIN", "LOSS", "TIE", "DRAW"
PRIMITIVES = (WIN, LOSS, TIE, DRAW)
UNKNOWN_REMOTENESS = -1

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
game_module = __import__(sys.argv[1].replace('.py', ''))

class GameState:
    """
    Wrapper for the idea of a GameState, not needed
    by the user, just makes things easier for the
    framework.
    """
    def __init__(self, pos):
        self.pos = pos
        self._state = None
        self._remoteness = None

    def get_hash(self):
        """
        Returns the appropriate hash of a given GameState object.
        Based off of the value of it's position.
        """
        return int(hashlib.md5(str(self.pos).encode('utf-8')).hexdigest(), 16) % size

    def expand(self):
        """
        Takes the current position and generates the
        children positions.
        """
        # Raw, in other words, not a GameState object.
        raw_states = map(lambda m: game_module.do_move(self.pos, m), game_module.gen_moves(self.pos))
        # Wrapped, in other words, a GameState object.
        wrapped_states = map(lambda m: GameState(m), raw_states)
        return wrapped_states

    @property
    def remoteness(self):
        """
        Determines returns remoteness if it
        has been found, returns UNKNOWN_REMOTENESS
        otherwise
        """
        if self._remoteness == None:
            return UNKNOWN_REMOTENESS
        else:
            return self._remoteness

    @remoteness.setter
    def remoteness(self, new_remoteness):
        self._remoteness = new_remoteness

    @property
    def state(self):
        """
        Determines whether the state is a:
        WIN, LOSS, TIE, DRAW or UNDECIDED
        """
        if self._state == None:
            return game_module.primitive(self.pos)
        else:
            return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def is_primitive(self):
        """
        Determines the difference between
        WLTD and UNDECIDED
        """
        # TODO: Don't violate abstraction barrier...
        # Notably: ("WIN", "LOSS", "TIE", "DRAW")
        return self.state in PRIMITIVES
