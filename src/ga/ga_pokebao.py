import numpy as np
from copy import deepcopy
from typing import Tuple, Dict, List
import random
from inspyred import ec, benchmarks

from data import dataset
from data.pokemon import Pokemon

class GAPokebao:
    def __init__(self, random):
        ec.GA.__init__(self, random)
        self.bounder = ec.DiscreteBounder([1, 151])
        teamAT=[]
        teamDF=[]

    def evaluator(candidates, args):
        # Evaluamos cada individuo con la suma de sus genes
        return [sum(ind) for ind in candidates]

    # Generador de individuos
    def generator(random, args):
        teamAT=[]
        while i<6
            pokemon=random.choice.(dataset.get_all_pokemons())
            while j<6
                if(teamAT[i]!=Pokemon)
                   pokemon=random.choice.(dataset.get_all_pokemons())
            teamAT[i].append(pokemon)
        return  teamAT # Individuo de 5 genes

    