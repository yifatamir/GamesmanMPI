from mpi4py import MPI
from game_state.game_state import GameState
from process.process import Process
from process.job import Job
import sys
import inspect
import logging
import imp

# Import game definition from file specified in command line
game_module = imp.load_source('game_module', sys.argv[1])

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

# Set up our logging system
logging.basicConfig(filename='logs/solver_log' + str(rank) + '.log', filemode='w', level=logging.WARNING)

initial_position = game_module.initial_position()

process = Process(rank, size)
if process.rank == Process.ROOT:
    initial_gamestate = GameState(initial_position)
    initial_job = Job(Job.LOOK_UP, initial_gamestate, process.rank, 0) # Defaults at zero, TODO: Fix abstraction violation.
    process.add_job(initial_job)

process.run()
