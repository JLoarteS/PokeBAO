import numpy as np
from copy import deepcopy
from typing import Tuple, List

from data import dataset
from data.pokemon import Pokemon, Move

POKES_IN_TEAM = 6
MOVES_IN_POKE = 4

class ACOPokebao:
    def __init__(self, def_team, all_pokemons = dataset.get_all_pokemons(), n_ants: int = 10, alpha: float = 1, beta: float = 5, rho: float = 0.8, n_cicles_no_improve: int = 50):
        self.def_team = def_team
        self.all_pokemons = all_pokemons
        
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.n_cicles_no_improve = n_cicles_no_improve

        self.pheromone_poke = None
        self.pheromone_move = None
        self.heuristic_poke = None
        self.heuristic_move = None

        self.best_solution = None
        self.best_fitness = None

        self.n_evaluations = 0
        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

    def optimize(self, max_evaluations: int = 100) -> List[Pokemon]:
        self._initialize()

        self.n_evaluations = 0
        while self.n_evaluations < max_evaluations and not self._stop_condition():
            trails = []
            for _ in range(self.n_ants):
                solution = self._construct_solution()
                fitness = self._evaluate(solution, self.def_team)
                self.n_evaluations += 1
                trails.append((solution, fitness))

                if fitness > self.best_fitness:
                    self.best_solution = solution
                    self.best_fitness = fitness

            self._update_pheromone(trails)

            self.trails_history.append(deepcopy(trails))
            self.best_fitness_history.append(self.best_fitness)

        return self.best_solution

    def _initialize(self):
        self.best_solution = []
        self.best_fitness = float('-inf') # -Infinite to maximise the solution

        self.pheromone_poke = np.ones(len(self.all_pokemons)) # List inizializated to ones, one per pokemon
        self.heuristic_poke = self._heuristic_pokemon() # List with a value for each pokemon, with the average strength of their moves
        self.pheromone_move = self._pheromone_move() # List inizializated to ones, one per move of each pokemon
        self.heuristic_move = self._heuristic_move() # Lista con un valor por cada move de cada poke, cuanto más potente más valor

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

    def _stop_condition(self) -> bool:
        """
        Check if the N last iterations did not improve the best solution
        """
        if len(self.best_fitness_history) < self.n_cicles_no_improve:
          return False
        
        stop_condition = np.all(np.isclose(self.best_fitness_history[-self.n_cicles_no_improve:], self.best_fitness))
  
        return stop_condition

    def _evaluate(self, solution: List[Pokemon], def_team: List[Pokemon]) -> float:
        """
        Calculates the total damage of our team to the defending team
        """
        fitness = 0
        
        for i in range(len(solution)):
            for j in range(len(def_team)):
                fitness += solution[i].damage_calculation(def_team[j])

        return fitness

    def _construct_solution(self) -> List[int]:
        """
        Constructs a solution where you first choose the pokemon team, and then their best moves from each one
        """
        solution_poke = []

        while len(solution_poke) < POKES_IN_TEAM:
            candidates = self._get_candidates_poke(solution_poke)

            pheromones = self.pheromone_poke[[self.all_pokemons.index(c) for c in candidates]]**self.alpha
            heuristic = self.heuristic_poke[[self.all_pokemons.index(c) for c in candidates]]**self.beta

            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total

            solution_poke.append(np.random.choice(candidates, p=probabilities))

        i = 0
        j = 0

        while i < POKES_IN_TEAM:
            # Position of the pokemon in the list of all pokemons
            idx = self.all_pokemons.index(solution_poke[i])

            while j < MOVES_IN_POKE:
                candidates = self._get_candidates_move(solution_poke[i])

                if len(candidates) == 0:
                    break
                elif len(candidates) == 1:
                    solution_poke[i].add_move(candidates[0])
                    break

                pheromones = self.pheromone_move[idx][[solution_poke[i].all_moves.index(c) for c in candidates]]**self.alpha
                heuristic = self.heuristic_move[idx][[solution_poke[i].all_moves.index(c) for c in candidates]]**self.beta

                total = np.sum(pheromones * heuristic)
                probabilities = (pheromones * heuristic) / total

                solution_poke[i].add_move(np.random.choice(candidates, p=probabilities).name)
                j += 1
            i += 1

        return solution_poke
    
    def _get_candidates_poke(self, solution_poke : List[Pokemon]) -> List[Pokemon]:
        candidates = List(set(self.all_pokemons) - set(solution_poke))
        return candidates
    
    def _get_candidates_move(self, pokemon: Pokemon) -> List[Move]:
        candidates = List(set(pokemon.all_moves) - set(pokemon.moves))
        return candidates

    def _update_pheromone(self, trails: Tuple[List[Pokemon], float]):
        self.pheromone_history.append(self.pheromone_poke.copy())

        evaporation = 1 - self.rho
        self.pheromone_poke *= evaporation
        for solution, fitness in trails:
            delta_fitness = 1.0/(1.0 + (self.best_fitness - fitness) / self.best_fitness)
            mask = np.argwhere(solution == 1).flatten()
            self.pheromone_poke[mask] += delta_fitness

    def _pheromone_move(self) -> List[List[int]]:
        """
        For each pokemon create a list of ones of all their moves
        """
        move_pheromone = []

        for pokemon in self.all_pokemons:
            move_pheromone.append(np.ones(len(pokemon.all_moves)))

        return move_pheromone

    def _heuristic_pokemon(self) -> List[float]:
        """
        Calculates the average power of all the pokemon's moves.
        """
        heuri_poke = []

        for pokemon in self.all_pokemons:
            heuri_poke.append(self._get_heuristic_poke(pokemon))

        return np.array(heuri_poke)
   
    def _get_heuristic_poke(self, poke : Pokemon) -> float:
        """
        Calculates the average power of all the pokemon's moves
        """
        sol = 0
        
        if len(poke.all_moves) == 0:
            print(f"No movements: {poke.name}")
            return 0

        for i in range(len(poke.all_moves)):
            sol += poke.all_moves[i].power

        return sol/len(poke.all_moves)
    
    def _heuristic_move(self) -> List[List[int]]:
        """
        Calculates the average power of all the pokemon's moves
        """
        heuri_move = []

        for i in range(len(self.all_pokemons)):
            aux = []
            for move in self.all_pokemons[i].all_moves:
                aux.append(move.power)
            heuri_move.append(np.array(aux))

        return heuri_move