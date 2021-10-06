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

from the parent folder (example for the MiniMax implementation). (Note that this way to execute the scripts may lead to import problems)


#### TO-DO

Some interesting things to do in order to upgrade this repo and make more readable could be:


- [ ] Investigate the recursion problems found in `RAVE`.

- [ ] Add `Makefile`.

- [ ] Implement `Lichess API` with different methods for online interactive playing.

- [ ] Define evaluation functions and pass them as argument to MiniMax players.

- [X] Create a `Game` class receiving two `Player` objects and generating a full game (with possibility of interactivity in Lichess).

- [X] Add `setup.py`.

- [X] Test MiniMax implementation.

- [X] Create a `Player` abstract class and use it to implement the algos.

- [X] Documentation.

- [X] Implement `RandomPlayer`.
