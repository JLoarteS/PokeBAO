import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List
import random
from inspyred import ec, benchmarks

from data import dataset
from data.pokemon import Pokemon

AMOUNT_TEAMS = 6
POKES_IN_TEAM = 6

class GAPokebao:
    def __init__(self):
        ec.GA.__init__(self, random)
        self.bounder = ec.DiscreteBounder([1, 151])
        teamAT=[]
        teamDF=[] # TODO: Hacer algo parecido a aco_experiment_executer para inicializar el equipo de 'smogon' 'reddit' o 'all'

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
            j = 0

            while j < POKES_IN_TEAM :

                if(teamAT[i]!=Pokemon):
                   pokemon=random.choice(dataset.get_all_pokemons())

            teamAT[i].append(pokemon)

        return  teamAT # Individuo de 5 genes
    
    def crossover(self, teams_pull : list[list[Pokemon]]):
        
        #for team in teams_pull:
            

        return
    
    def pokes_corssover(self, team_1: list[Pokemon], team_2: list[Pokemon]):
        
        return
    
    def moves_crossover(self):

        return

    def pokes_mutation(self):
        
        return
    
    def moves_mutation(self):

        return
    