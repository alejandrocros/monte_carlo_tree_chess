# Monte Carlo Tree Search Methods for Chess

In this repo I will share the code for some implementations of Monte Carlo Tree Seach algorithms for playing chess.

The source code is stored in `mctchess`, where we define the `Player` class and implement multiple game algorithms.

Useful notebooks will be stored in the `/notebooks` folder:
- The notebook `MCTS_Code.ipynb` stores some useful code to implement the algorithms (the main part of it already migrated to the `mctchess` folder).

- The notebook `UTC_comparison.ipynb` generates the graphics for the UTC experiments.

### Execution

In order to execute a specific algorithm, one needs to install the package:

```bash
pip install -e .
```

and running the desired script as:

```bash
python mctchess/minimax_implementation.py
```

Another alternative execution procedure consists on installing only the requirements (not the entire package) and running the desired script as follows:

```bash
python -m mctchess.minimax_implementation
```

from the parent folder (example for the MiniMax implementation). (Note that this way to execute the scripts may lead to import problems).

The different players are stored in the directory `mctchess.players`. We can use them to play a `Game` as follows:

```python
from chess import Board

from mctchess.game.game import Game
from mctchess.players.monte_carlo_player import MCPlayer

p_white = MiniMaxPlayer(depth=2, add_mobility=False, ab_pruning=True)
p_black = MCPlayer(n_simulations=1000, no_pools=3)

initial_board = Board()
game = Game(p_white, p_black, board, verbose=False) # Creating the Game object
game.play_game() # game rollout
winner = board.outcome().winner # in this case it was False, corresponding to the black player (Monte-Carlo based).
```

In the `notebooks` directory there are different examples of how to use players and compare their performance.


#### Under development

Some interesting things to do in order to upgrade this repo and make more readable are:


- [ ] Put the evaluation arguments inside a method that calls eval function.

- [ ] Investigate the recursion problems found in `RAVE`.

- [ ] Implement `Lichess API` with different methods for online interactive playing.

- [ ] Add hashing of positions with evaluation in `Game` to enhance performance.

- [ ] Refactor evaluation functions and pass them as argument to MiniMax players.

- [ ] Add square value to piece evaluation (use board.piece_map() and values stored in a dict)

- [ ] Add parallel computation for minimax and for game simulation.

- [ ] Put minimax and minimax_pruned out of MiniMaxPlayer.

- [ ] Perf comparison of parallel - no parallel MC implementation (profiling in notebook?).

- [X] Parallelize Monte-Carlo evaluation.

- [X] Test MiniMax implementation.

- [X] Add alpha-beta pruning.
