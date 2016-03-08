from mpi4py import MPI
from src.game_state import GameState
from src.job import Job
from src.process import Process
import inspect
import logging
import imp
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("game_file", help="game to solve for")
parser.add_argument("-np", "--numpy", help="optimize for numpy array usage",
                               action="store_true")

args = parser.parse_args()

# Load file.
game_module = imp.load_source('game_module', args.game_file)

# Make sure the game is properly defined
assert(hasattr(game_module, 'initial_position'))
assert(hasattr(game_module, 'do_move'))
assert(hasattr(game_module, 'gen_moves'))
assert(hasattr(game_module, 'primitive'))
assert(inspect.isfunction(game_module.initial_position))
assert(inspect.isfunction(game_module.do_move))
assert(inspect.isfunction(game_module.gen_moves))
assert(inspect.isfunction(game_module.primitive))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

send = comm.send
recv = comm.recv

# Check for optimizations.
if args.numpy:
    send = comm.Send
    recv = comm.Recv

# Set up our logging system
logging.basicConfig(filename='logs/solver_log' + str(rank) + '.log', filemode='w', level=logging.WARNING)

initial_position = game_module.initial_position()

process = Process(rank, size, send, recv, comm)
if process.rank == process.root:
    initial_gamestate = GameState(initial_position)
    initial_job = Job(Job.LOOK_UP, initial_gamestate, process.rank, 0) # Defaults at zero, TODO: Fix abstraction violation.
    process.add_job(initial_job)

process.run()
