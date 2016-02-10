#################################################
# 4 - 1 Portion
# TODO: Move out of this file
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

#################################################
# SOLVER PORTION
#################################################

#################################################
# INITIALIZE
# We need to have the rank0 process start everyt-
# hing.
#################################################

from mpi4py import MPI
from heapq import heappush, heappop
import hashlib

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def move(pos, gen, do):
    """Combines do_move and gen_move."""
    return map(lambda m: do(pos, m), gen(pos))

class Job:
    def __init__(self, state, parent, priority=0):
        self.state = state
        self.parent = parent
        self.priority = priority

    def __cmp__(self, other):
        """ 
        Compares two Job objects based off the priority
        they have.
        """
        return cmp(self.priority, other.priority)

def distribute(jobs):
    """ 
    Given a list of jobs, distributes them to the cor-
    rect computer.
    """
    for job in jobs:
        to = int(hashlib(job.state).hexdigest(), 16) % size
        comm.send(job, to)

def wait_receive(job):
    # TODO
    pass

# The transposition table of resolved states.
resolved = {}

work = []

job = None
update_job = True

while True:
    if update_job:
        job = heappush(work)
    # Nothing to do.
    if job == None:
        continue
    # Look up
    if job.state in resolved:
        send_back(job, resolved)
    elif isinstance(job.state, list):
        # Wait to recv job results.
        update_job = wait_receive(job.state)
    else:
        children = move(job, gen_moves, do_move)
        distribute(children)
        new_job = Job(children, rank)

comm.Barrier()
