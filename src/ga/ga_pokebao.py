import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List
from inspyred import ec, benchmarks
import math
import random 
from time import time

from data import dataset
from data.pokemon import Pokemon

AMOUNT_TEAMS = 3
POKES_IN_TEAM = 6

class Pokebao(benchmarks.Benchmark):
    def __init__(self, def_team, all_pokemons):
        self.length = 6 * (1 * 4) # 6 Pokémon * (1 ID + 4 moves)
        benchmarks.Benchmark.__init__(self, dimensions=self.length)
        self.bounder = ec.DiscreteBounder([1, 151]) 
        self.permutation_bounder = ec.DiscreteBounder([i for i in range(self.length)])
        self.maximize = True

        self.def_team = def_team
        self.all_pokemons = all_pokemons
    
    def generator(self, random, args):
        """
        Return a candidate solution consisting of two parts: binary and permutation.
        """
        att_team = []
        i = 0

        while i < POKES_IN_TEAM:
            pokemon=random.choice(self.all_pokemons)

            if pokemon not in att_team:
                att_team.append(pokemon)
                i+=1
        
        for i in att_team:
            i.set_all_random_moves()
            
        return att_team

    def evaluator(self, candidates, args):
        """
        Return the fitness values for the given candidates.
        """
        fitness = []

        for team in candidates:
            aux = 0
            for poke in team:
                for defender in self.def_team:
                    aux += poke.damage_calculation(defender)
            fitness.append(aux)

        return fitness

class GAPokebao:    
    @classmethod
    def crossover(cls, random, candidates, args):
        crossover_rate = args['crossover_rate']
        return cls.pokebao_inspyred_crossover(candidates, crossover_rate)

    @classmethod
    def pokebao_inspyred_crossover(cls, candidates, crossover_rate):
        if len(candidates) % 2 == 1:
            candidates = candidates[:-1]

        moms = candidates[::2]
        dads = candidates[1::2]
        children = []

        for mom, dad in zip(moms, dads):
            if random.random() < crossover_rate:
                point = random.randint(1, len(mom) - 1)
                child1 = mom[:point] + dad[point:]
                child2 = dad[:point] + mom[point:]
            else:
                child1 = mom[:]
                child2 = dad[:]

            children.extend([child1, child2])

        return children

    @classmethod
    def mutation(cls, random, candidates, args):
        mutation_rate = args['mutation_rate']
        for team in candidates:
            cls.pokes_mutation(team, mutation_rate)

            for pokemon in team:
                cls.moves_mutation(pokemon, mutation_rate)
        
        return candidates

    @classmethod
    def pokes_mutation(cls, candidate: list[Pokemon], mutation_rate):
        for i in range(len(candidate)):
            if cls.posibility_to_enter(mutation_rate * 100):
                cls.change_a_poke(i, candidate)

        return candidate
    
    @classmethod
    def change_a_poke(cls, posi: int, team: list[Pokemon]):
        done = True
        while done:
            poke = random.choice(dataset.get_all_pokemons())
            if poke not in team:
                poke.set_all_random_moves()
                team[posi] = poke
                done = False  

        return team
    
    @classmethod
    def moves_mutation(cls, candidate: Pokemon, mutation_rate):
        if len(candidate.all_moves) > 4:
            for i in range(4):
                if cls.posibility_to_enter(mutation_rate * 100):
                    cls.change_a_move(i, candidate)

        return candidate
    
    @classmethod
    def change_a_move(cls, posi: int, poke: Pokemon):
        done = True
        while done:
            new_move = poke.get_random_move()
            if new_move not in poke.moves:
                poke.moves[posi] = new_move
                done = False  

        return poke
    
    @classmethod
    def posibility_to_enter(cls, posibility):
        if not 0 <= posibility <= 100:
          print("The value put in \"posibility\" must be between 0 y 100")
        return random.randint(1, 100) <= posibility
    
    def __init__(self, def_team, all_pokemons = dataset.get_all_pokemons(), **kwargs):
        self.def_team = def_team
        self.all_pokemons = all_pokemons

        self.problem = Pokebao(def_team, all_pokemons)

        self.pop_size = kwargs.get('pop_size', AMOUNT_TEAMS)
        self.selector = kwargs.get('selector', ec.selectors.tournament_selection)
        self.tournament_size = kwargs.get('tournament_size', 2)
        self.replacer = kwargs.get('replacer', ec.replacers.generational_replacement)
        self.num_elites = kwargs.get('num_elites', 1)
        self.terminator = kwargs.get('terminator', ec.terminators.no_improvement_termination)
        self.max_generations = kwargs.get('max_generations', 20)
        self.crossover = kwargs.get('crossover', GAPokebao.crossover)
        self.crossover_rate = kwargs.get('crossover_rate', 0.8)
        self.mutation = kwargs.get('mutation', GAPokebao.mutation)
        self.mutation_rate = kwargs.get('mutation_rate', 0.3)
        self.constraint_handler = kwargs.get('constraint_handler', "repair")
        self.best_fitness_history = []
        self.solutions_history = []
        self.num_evaluations = 0
        self.num_generations = 0
    
    def _initialize(self):
        self.best_fitness_history = []
        self.solutions_history = []
        self.num_evaluations = 0
        self.num_generations = 0

    def history_observer(self, population, num_generations, num_evaluations, args):
        """Observer to track best fitness and diversity."""
        best = max(population).fitness
        self.best_fitness_history.append(best)
        self.solutions_history.append([(deepcopy(i.candidate), i.fitness) for i in population])

    def run(self, seed=None):
        rand = random.Random()
        if seed is not None:
            rand.seed(seed)
        self._initialize()

        ga = ec.GA(rand)
        ga.terminator = self.terminator
        ga.observer = self.history_observer
        ga.selector = self.selector
        ga.replacer = self.replacer
        ga.variator = [self.crossover, self.mutation]
        final_pop = ga.evolve(generator=self.problem.generator,
                              evaluator=self.problem.evaluator,
                              pop_size=self.pop_size,
                              maximize=self.problem.maximize,
                              bounder=self.problem.bounder,
                              max_generations=self.max_generations,
                              num_elites=self.num_elites,
                              num_selected=self.pop_size,
                              tournament_size=self.tournament_size,
                              crossover_rate=self.crossover_rate,
                              mutation_rate=self.mutation_rate)
        self.num_generations = ga.num_generations
        self.num_evaluations = ga.num_evaluations
        best = max(final_pop)
        return best.candidate, best.fitness