# GamesmanMPI
### MPI-Based Solver for Two Player Abstract Strategy Games

(More project description here)

---

## Description of API
There are four elements which a game class must implement:
- initial_position
2. gen_moves
3. do_moves
4. primitive

The exact way in which you represent a game state (ints, lists, etc.) does not matter, as long as you are consistant. For the puposes of this guide, we'll use a generic "GameState" type.

#### initial_position
