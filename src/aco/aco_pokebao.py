import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List
import random

from data import dataset
from data.pokemon import Pokemon

"""
    Cosas que hay que pensar:
        Se necesita dos ACO en uno (Pokemon y Movimiento de Pokemon)
        1. Heuristica para el mejor Pokemon por cada tipo (maximizar por multiplicador de tipo)
        2. Heuristica para el movimiento para cada pokemon (maximizar por damage)
    
"""
class ACOPokebao:
    def __init__(self, all_pokemons = dataset.get_all_pokemons(), n_ants: int = 10, alpha: float = 1, beta: float = 5, rho: float = 0.8):
        
        self.all_pokemons = all_pokemons
        #self.def_team = def_team
        
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        
        self.n_evaluations = 0

        self.pheromone_poke = np.ones(len(all_pokemons)) #Lista inicializada a unos, uno por poke
        self.pheromone_move = self._phero_move_ini #Lista inicializada a unos, uno por move de cada poke
        self.heuristic_poke = self._heuristic_poke_ini #Lista con un valor por poke, en el que segun lo bueno que sea un poke, valor (a ver como)
        self.heuristic_move = self._heuristic_move_ini #Lista con un valor por cada move de cada poke, cuanto más potente más valor


        self.best_solution = None
        self.best_fitness = None

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

        self.team = []

    def optimize(self, max_evaluations: int = 1000):
        self._initialize()

        n_evaluations = 0
        while n_evaluations < max_evaluations:
        # while n_evaluations < max_evaluations and not self._stop_condition(): ##### TODO Poner al final para para cuando se estaque o cambiar cuando encuentra un minimo local
            trails = []
            for _ in range(self.n_ants):
                solution = self._construct_solution()
                fitness = self._evaluate(solution)
                n_evaluations += 1
                trails.append((solution, fitness))

                if fitness > self.best_fitness:
                    self.best_solution = solution
                    self.best_fitness = fitness

            self._update_pheromone(trails, self.best_fitness)

            self.trails_history.append(deepcopy(trails))
            self.best_fitness_history.append(self.best_fitness)

        return self.best_solution

    def _initialize(self):
        self.pheromone = None ##### TODO Rellenar con las pheromonas
        self.best_solution = None
        self.best_fitness = float('-inf') # -Infinite to maximise the solution

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

    def _stop_condition(self) -> bool:
        """
        Check if the N last iterations did not improve the best solution
        """
        pass

    def _evaluate(self, solution: Tuple[List[int], List[int]]) -> float:
        """
        Calculates the inverse end time of the sword that is forged last
        """
        ##### TODO CAMBIAR el solution y aqui poner el calculo del daño
        pass

    def _construct_solution(self) -> List[int]:
        """
        Constructs a solution by combining the worker assignment and forging order parts
        """
        ##### TODO CAMBIAR el type del return (solution) y poner esto bien
        solution_poke = []
        solution_move = []

        while len(solution_poke) < 6:
            candidates = self._get_candidates(solution_poke)

            pheromones = self.pheromone_poke[candidates]**self.alpha
            heuristic = self._heuristic(candidates)**self.beta

            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total

            solution_poke[np.random.choice(candidates, p=probabilities)] = 1

        while len(solution_move) < 6:
            candidates = self._get_candidates(solution_move)

            pheromones = self.pheromone_move[candidates]**self.alpha
            heuristic = self._heuristic(candidates)**self.beta

            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total

            solution_move[np.random.choice(candidates, p=probabilities)] = 1

        return Tuple[solution_poke, solution_move]
    
    def _get_candidates(self, _):
        candidates = list(set(dataset.get_all_pokemons()) - set(self.team))
        return candidates

    def _update_pheromone(self, trails: List[List[int]], best_fitness):
        self.pheromone_history.append(self.pheromone.copy())

        evaporation = 1 - self.rho
        self.pheromone *= evaporation
        for solution, fitness in trails:
            delta_fitness = 1.0/(1.0 + (best_fitness - fitness) / best_fitness)
            mask = np.argwhere(solution == 1).flatten()
            self.pheromone[mask] += delta_fitness

    def _phero_move_ini(self):
        
        move_pheromone = []

        for i in len(self.all_pokemons):
            move_pheromone[i] = np.ones(len(self.all_pokemons[i].all_moves))

        return move_pheromone

    def _heuristic_poke_ini(self):
        heuri_poke = []

        for i in len(self.all_pokemons):
            heuri_poke.append(self.get_heuri_poke(self.all_pokemons[i]))

        return heuri_poke
    
    def get_heuri_poke(self, poke : Pokemon):
        sol = 0

        for i in len(poke.all_moves):
            sol += poke.all_moves[i].power

        return sol
    
    def _heuristic_move_ini(self):
        heuri_move = []

        for i in len(self.all_pokemons):
            aux = []
            for j in len(self.all_pokemons[i].all_moves):
                aux[j] = self.all_pokemons[i].all_moves[j].power
            heuri_move[i] = aux

        return heuri_move