<h1>PokeBao<img src="https://www.pngplay.com/wp-content/uploads/10/Blastoise-Pokemon-Background-PNG.png" alt="Blastoise" align="right" width="150"/></h1>

This repository addresses the problem of building an offensively optimal Pokémon team to face a predetermined enemy team. The goal is to select a team of 6 Pokémon
that maximizes offensive effectiveness against an opposing group that can include between 6 and up to 72 different Pokémon.

This is for a project for the "Bio-inspired Algorithms for Optimisation" course at the Polytechnic University of Madrid.

<hr>

## Dataset

The defending teams are taken from [Smogon](https://www.smogon.com/forums/threads/rby-ou-sample-teams.3689726/ "List of the best teams")
or from this [Reedit Thread](https://www.reddit.com/r/pokemon/comments/7utxq6/your_best_gen_1_teams/).

For the damage function, we have taken it from [Bulbapedia.Bulbagarden](https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_I).

Finally, for all the Pokémon data we have collected it from the [PokeAPI](https://pokeapi.co), and to transform it into `.json`
we have used the [Pokebase](https://github.com/PokeAPI/pokebase) module for python.

## Folders and files

The repository contains the following folders and files:

- `src`: This folder contains all the code to solve the problem.
  - `src/ga`: This folder contains the implementation of GA for solving the problem.
  - `src/aco`: This folder contains the implementation of ACO for solving the problem.
  - `src/experiment`: This folder contains code for experimental testing of the algorithms.
- `data`: This folder contains the datasets used in the experiments.
- `experiments`: This folder contains the results of the experiments.
- `run_ga.ipynb`: This file contains the code for running the GA algorithm.
- `run_aco.ipynb`: This file contains the code for running the ACO algorithm.
- `compare_results.ipynb`: This file contains the code for statistically comparing the results achieved by the algorithms, and also plotting the results.
