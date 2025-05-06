import pandas as pd
from typing import Dict
import random

from src.aco.aco_pokebao import ACOPokebao
import data.dataset as dataset
from data.pokemon import Pokemon

class ACOExperimentExecuter:
    
    def __init__(self):
        self.dataset_pokemons = dataset.get_all_pokemons()
        self.dataset_movements = dataset.get_all_movements()
        self.type_matrix = dataset.get_types_matrix()

    def run_single_experiment(self, def_team_experiment: str, num_defenders=6, n_ants=10, alpha=0.5, beta=1.0, rho=0.75, n_cicles_no_improve=50) -> pd.DataFrame:
        """
        Runs an experiment with the given ACO algorithm and dataset.
        Returns the best solution find in the experiment.
        """
        def_team = self._read_defenders_data(def_team_experiment, self.dataset_pokemons, num_defenders)
        
        aco = ACOPokebao(
            all_pokemons=self.dataset_pokemons,
            def_team=def_team,
            n_ants=n_ants,
            alpha=alpha,
            beta=beta,
            rho=rho,
            n_cicles_no_improve=n_cicles_no_improve
        )
        aco.optimize()
        return aco
    
    def run_repeated_experiment(self, def_team_experiment: str, num_defenders=6, n_repeat=31, n_ants=10, alpha=0.5, beta=1.0, rho=0.75, n_cicles_no_improve=50) -> pd.DataFrame:
        """
        Runs an experiment with the given ACO algorithm and dataset n_repeat times.
        Returns a DataFrame with the fitness and number of cicles of each run.
        """
        results = [] 
        for i in range(n_repeat):
            print(f"Running experiment: dataset {def_team_experiment} - run {i+1}/{n_repeat}")
            aco = self.run_single_experiment(def_team_experiment, num_defenders, n_ants, alpha, beta, rho, n_cicles_no_improve)
            actual_result = {
                "run": i,
                "fitness": 1.0/aco.best_fitness,
                "n_evaluations": aco.n_evaluations
            }
            results.append(actual_result)

        return pd.DataFrame(results)
    
    def run_all_experiment(self, n_repeat=31, n_ants=10, alpha=0.5, beta=1.0, rho=0.75, n_cicles_no_improve=50) -> pd.DataFrame:
        """
        Runs an experiment with the given ACO algorithm and all dataset n_repeat times.
        Returns a DataFrame with the fitness and number of cicles of each run.
        """
        results = [] 
        for i in range(n_repeat):
            print(f"Running experiment: dataset all - run {i+1}/{n_repeat}")
            aco = self.run_single_experiment("all", 6, n_ants, alpha, beta, rho, n_cicles_no_improve)
            actual_result = {
                "run": i,
                "fitness": 1.0/aco.best_fitness,
                "n_evaluations": aco.n_evaluations
            }
            results.append(actual_result)

        return pd.DataFrame(results)

    def _read_defenders_data(self, def_team_experiment: int, all_pokemons: list[Pokemon], num_leaders: int = 6) -> list[Pokemon]:
        
        def_team = []
        
        # Read CSV
        if def_team_experiment != "all":
            data = pd.read_csv(f"src/experiment/def_teams_{def_team_experiment}.csv", delimiter=';')
            
            # Get list[list] of leaders and his pokemons
            data_leaders = data.groupby('id_leader')['pokemon'].apply(list).to_list()
        else:
            data_reedit = pd.read_csv(f"src/experiment/def_teams_reedit.csv", delimiter=';')
            data_smogon = pd.read_csv(f"src/experiment/def_teams_smogon.csv", delimiter=';')

            data_leaders_reedit = data_reedit.groupby('id_leader')['pokemon'].apply(list).to_list()
            data_leaders_smogon = data_smogon.groupby('id_leader')['pokemon'].apply(list).to_list()
            
            # Get list[list] of leaders and his pokemons
            data_leaders = data_leaders_reedit + data_leaders_smogon
        
        # Shuffle the leaders to randomize the experiments
        random.shuffle(data_leaders)
        
        # Concat all the pokemons names from all chosen leaders
        pokemons_names = [pokemon for leaders in data_leaders[:num_leaders] for pokemon in leaders]
        print(pokemons_names)
        print(len(pokemons_names))
        
        # Create a list with Pokemon object from the leaders' pokemons
        def_team = []

        # Find the Pokemon object from the all_pokemons data
        for name in pokemons_names:
            for pokemon in all_pokemons:
                if pokemon.name == name:
                    def_team.append(pokemon)
                    break
        
        return def_team