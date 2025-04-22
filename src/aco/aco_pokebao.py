import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List

"""
    Cosas que hay que pensar:
        Se necesita dos ACO en uno (Pokemon y Movimiento de Pokemon)
        1. Heuristica para el mejor Pokemon por cada tipo (maximizar por multiplicador de tipo)
        2. Heuristica para el movimiento para cada pokemon (maximizar por damage)
    
"""
class ACOPokebao:
    def __init__(self, n_ants: int = 10, alpha: float = 1, beta: float = 5, rho: float = 0.8):
        
        ##### TODO Falta aqui lo necesario para realizar el algoritmo (ponerlo antes de n_ants)
        
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        
        self.n_evaluations = 0

        self.pheromone = None
        self.best_solution = None
        self.best_fitness = None

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

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
        solution = np.zeros(len(self.weights))

        while True:
            candidates = self._get_candidates(solution)

            if len(candidates) == 0:
                break
            elif len(candidates) == 1:
                solution[candidates[0]] = 1
                break

            pheromones = self.pheromone[candidates]**self.alpha
            heuristic = self._heuristic(candidates)**self.beta

            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total

            solution[np.random.choice(candidates, p=probabilities)] = 1

        return solution
    
    def _get_candidates(self, _):
        ##### TODO CAMBIAR 
        candidates = []

        return candidates

    def _heuristic(self, candidates: List[int]) -> np.ndarray:
        pass

    def _update_pheromone(self, trails: List[List[int]], best_fitness):
        self.pheromone_history.append(self.pheromone.copy())

        evaporation = 1 - self.rho
        self.pheromone *= evaporation
        for solution, fitness in trails:
            delta_fitness = 1.0/(1.0 + (best_fitness - fitness) / best_fitness)
            mask = np.argwhere(solution == 1).flatten()
            self.pheromone[mask] += delta_fitness