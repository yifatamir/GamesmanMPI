# GamesmanMPI
### MPI-Based Solver for Two Player Abstract Strategy Games

(More project description here)

## Loading a Game
Games to be solved are loaded via the command line, with the following syntax:
```
python solver.py <your game file>
```
For example, you could load our example game, Four-To-One, by running
```
python solver.py four_to_one.py
```

Your game file must follow the conventions outlined in the API 

## Description of API
There are four elements which a game class must implement:
- initial_position
2. gen_moves
3. do_moves
4. primitive

The exact way in which you represent a game state or moves (ints, lists, etc.) does not matter, as long as you are consistant. For the puposes of this guide, we'll use an integer to represent our gamestate and moves, since we our example is Four-To-One.

#### initial_position
This is simply a consant value of your gamestate type. In Four-To-One, we define it as
```python
initial_position = 4
```
#### gen_moves( *gs* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate for which you are generating moves
- returns: *list of move-type*
  - All legal moves from that gamestate

###### Example
```python
def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]
```

#### do_move( *gs*, *m* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate from which you are making a move
- m: *move-type*
  - The move that you are making
- returns: *gamestate-type*
  - The new gamestate after the move has been made

###### Example
```python
def do_move(x, move):
    return x + move
```
#### primitive( *gs* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate that you are analyzing
- returns: *list of move-type*
  - The primitive type for *gs*, if it is a pimitive (WIN, LOSS, TIE, DRAW)

###### Example
```python
def primitive(x):
    if x <= 0:
        return LOSS
```
