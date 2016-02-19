#################################################
# SOLVER PORTION
#################################################

DEBUG = True

from mpi4py import MPI
import hashlib
import sys
import inspect
from queue import PriorityQueue

# Import game definition from file specified in command line
game_module = __import__(sys.argv[1].replace('.py', ''))

# Make sure the game is properly defined
assert(hasattr(game_module, 'initial_position'))
assert(hasattr(game_module, 'do_move'))
assert(hasattr(game_module, 'gen_moves'))
assert(hasattr(game_module, 'primitive'))
assert(inspect.isfunction(game_module.do_move))
assert(inspect.isfunction(game_module.gen_moves))
assert(inspect.isfunction(game_module.primitive))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

class GameState:
    """
    Wrapper for the idea of a GameState, not needed
    by the user, just makes things easier for the
    framework.
    """
    def __init__(self, pos):
        self.pos = pos

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
    def state(self):
        """
        Determines whether the state is a:
        WIN, LOSS, TIE, DRAW or UNDECIDED
        """
        return game_module.primitive(self.pos)

    def is_primitive(self):
        """
        Determines the difference between
        WLTD and UNDECIDED
        """
        # TODO: Don't violate abstraction barrier...
        # Notably: ("WIN", "LOSS", "TIE", "DRAW")
        return self.state in ("WIN", "LOSS", "TIE", "DRAW")

class Job:
    """
    A job has a game state, parent, type, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """
    # A list of possible job types.
    LOOK_UP           = "lookup"
    DISTRIBUTE        = "distribute"
    CHECK_FOR_UPDATES = "check_for_updates"
    SEND_BACK         = "send_back"
    FINISHED          = "finished"
    _priority_table = {
            FINISHED          : 0,
            LOOK_UP           : 1,
            SEND_BACK         : 2,
            DISTRIBUTE        : 3,
            CHECK_FOR_UPDATES : 4
    }

    # Keep a special variable for the initial job!
    # This way you can check if the job you finished was
    # the initial job. In this case we are done!
    INITIAL_JOB_ID = -1

    def _assign_priority(self):
        self.priority = self._priority_table[self.job_type]

    def __init__(self, job_type, game_state=None, parent=None, job_id=None):
        self.job_type   = job_type
        self.game_state = game_state
        self.parent     = parent
        self.job_id     = job_id
        self._assign_priority()

    def __lt__(self, other):
        """
        Compares two Job objects based off the priority
        they have.
        """
        return self.priority < other.priority

class Process:
    """
    Class that defines the behavior what each process should do
    """
    ROOT = 0
    IS_FINISHED = False

    def dispatch(self, job):
        """
        Given a particular kind of job, decide what to do with
        it, this can range from lookup, to distributing, to
        checking for recieving.
        """
        _dispatch_table = {
                Job.FINISHED          : self.finished,
                Job.LOOK_UP           : self.lookup,
                Job.DISTRIBUTE        : self.distribute,
                Job.SEND_BACK         : self.send_back,
                Job.CHECK_FOR_UPDATES : self.check_for_updates
        }
        return _dispatch_table[job.job_type](job)


    def run(self):
        """
        Main loop for each process
        """
        # TODO
        while not Process.IS_FINISHED:
            if self.work.qsize() == 0:
                # Either we are done...
                if self.rank == Process.ROOT:
                    if DEBUG:
                        print("Finished")
                    fin = Job(Job.FINISHED)
                    for r in range(0, size):
                        comm.isend(fin,  dest = r)
                # ... or we must wait.
                else:
                    self.add_job(Job(Job.CHECK_FOR_UPDATES))
            job = self.work.get()
            result = self.dispatch(job)
            if result is None: # Check for updates returns nothing.
                continue
            self.add_job(result)

    def __init__(self, rank):
        self.rank = rank
        self.work = PriorityQueue()
        self.resolved = {}
        # Keep a list of sent requests, and received requests,
        # if sending fails, should be able to handle it some-
        # how.
        # As for recieving, should test them when appropriate
        # in the run loop.
        self.sent = []
        self.received = []
        # Keep a dictionary of "distributed tasks"
        # Should contain an id associated with the length of task.
        # For example, you distributed rank 0 has 4, you wish to
        # distribute 3, 2. Give it an id, like 1 and associate it
        # with length 2. Then once all the results have been received
        # you can compare the length, and then reduce the results.
        # solving this particular distributed task.
        self._distributed = {}
        self._distributed_id = 0
        # Main process will terminate everyone by bcasting the value of
        # finished to True.
        self.finished = False

    def add_job(self, job):
        """
        Adds a job to the priority queue so it may be worked on at an
        appropriate time
        """
        self.work.put(job)

    def finished(self, job):
        """
        Occurs when the root node has detected that the game has been solved
        """
        IS_FINISHED = True

    def lookup(self, job):
        """
        Takes a GameState object and determines if it is in the
        resolved list. Returns the result if this is the case, None
        otherwise.
        """
        if DEBUG:
            print("Machine " + str(rank) + " looking up " + str(job.game_state.pos))
        try:
            res = self.resolved[job.game_state.pos]
            if DEBUG:
                print(str(job.game_state.pos) + " has been resolved")
            return Job(Job.SEND_BACK, res, self.rank, job.parent, job.job_id)
        except KeyError: # Not in dictionary.
            # Try to see if it is_primitive:
            if job.game_state.is_primitive():
                if DEBUG:
                    print(str(job.game_state.pos) + " is primitive")
                self.resolved[job.game_state.pos] = job.game_state.state
                return Job(Job.SEND_BACK, job.game_state.state, self.rank, job.job_id)
            self._distributed_id += 1
            return Job(Job.DISTRIBUTE, job.game_state, self.rank, self._distributed_id)

    def distribute(self, job):
        """
        Given a gamestate distributes the results to the appropriate
        children.
        """
        children = job.game_state.expand()
        # Keep a list of the requests made by isend. Something may
        # fail, so we will need to worry about error checking at
        # some point.
        for child in children:
            job = Job(Job.LOOK_UP, child, self.rank, self._distributed_id)
            if DEBUG:
                print(str(rank) + " found child " + str(job.game_state.pos) + ", sending to " + str(child.get_hash()))

            self.sent.append(comm.isend(job,  dest = child.get_hash()))

    def check_for_updates(self, job):
        """
        Checks if there is new data from other Processes that needs to
        be received and prepares to recieve it if there is any new data.
        Returns True if there is new data to be recieved.
        Returns None if there is nothing to be recieved.
        """
        # Probe for any sources

        if comm.iprobe(source=MPI.ANY_SOURCE):
            # If there are sources recieve them.
            self.received.append(comm.recv(source=MPI.ANY_SOURCE))
            for job in self.received:
                self.add_job(job)

            self.recieved = [] # Clear recieved.

    def send_back(self, job):
        """
        Send the job back to the node who asked for the computation
        to be done.
        """
        if DEBUG:
            print(str(rank) + " is sending back " + str(job.game_state.pos))
        comm.send(job, dest=job.parent)

    def _res_red(self, res1, res2):
        """
        Private method that helps reduce in reduce_results.
        """
        # Probably can be done in a "cleaner" way.
        if res1 == "LOSS" and res2 == "LOSS":
            return "LOSS"
        elif res1 == "WIN" or res2 == "WIN":
            return "WIN"
        elif res1 == "TIE" or res2 == "TIE":
            return "TIE"
        elif res1 == "DRAW" or res2 == "DRAW":
            return "DRAW"

    def reduce_results(self, results):
        """
        Given a list of WIN, LOSS, TIE, (DRAW, well maybe for later)
        determine whether this position in the game tree is a WIN,
        LOSS, TIE, or DRAW.
        """
        # TODO for TIE, DRAW
        return reduce(results, _res_red)


process = Process(rank)
if process.rank == Process.ROOT:
    initial_gamestate = GameState(game_module.initial_position)
    initial_job = Job(Job.LOOK_UP, initial_gamestate, process.rank, Job.INITIAL_JOB_ID)
    process.add_job(initial_job)

process.run()

comm.Barrier()
