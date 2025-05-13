import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List
import random
from inspyred import ec, benchmarks

from data import dataset
from data.pokemon import Pokemon

AMOUNT_TEAMS = 50
POKES_IN_TEAM = 6
CROSSOVER_VALUE = 0.7

class GAPokebao:
    def __init__(self,def_team, all_pokemons = dataset.get_all_pokemons()):
        ec.GA.__init__(self, )
        self.bounder = ec.DiscreteBounder([1, 151])
        teamAT=[]
        self.def_team = def_team

    def evaluator(self, team : list[Pokemon]):
        # Evaluamos cada individuo con la suma de sus genes

        fitness = []

        for i in range(len(team)):
            for j in range(len(self.teamDF)):
                fitness += team[i].damage_calculation(self.teamDF[j])

        return fitness
    
    def team_pull_generator(self):

        team_pull = list[list[Pokemon]]

        for i in AMOUNT_TEAMS:
            team_pull.append(self.team_generator())

        return team_pull

    # Generador de individuos
    def team_generator(self):

        teamAT=[]

        i = 0

        while i < POKES_IN_TEAM:

            pokemon=random.choice(dataset.get_all_pokemons())

            if (pokemon not in teamAT):
                teamAT[i].append(pokemon)
                i+=1
            
        return  teamAT # Individuo de 5 genes
    
    def crossover(self, teams_pull : list[list[Pokemon]]):
        
        return self.inspyred_crossover(random, teams_pull)


    def pokes_mutation(self, candidate: list[Pokemon]):
        # TODO: comprobar si muta o no y luego cambiar a otro pokemon con movimientos random prehechos

        return
    
    def moves_mutation(self, candidate: Pokemon):
        # TODO: comprobar si muta o no y luego cambiar a otro movimiento del mismo pokemon

        return
    

    def inspyred_crossover(random, candidates, args):
        if len(candidates) % 2 == 1:
            candidates = candidates[:-1]
        moms = candidates[::2]
        dads = candidates[1::2]
        children = []
        for i, (mom, dad) in enumerate(zip(moms, dads)):
            np.cross.index = i
            offspring = np.cross(random, mom, dad, args)
            for o in offspring:
                children.append(o)
        return children