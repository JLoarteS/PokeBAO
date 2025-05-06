import pandas as pd
import shutil
from os import makedirs
from os.path import isdir
from typing import Dict, Tuple

from src.aco.aco_pokebao import ACOPokebao
import data.dataset as dataset


class ACOExperimentExecuter:
    
    def __init__(self):
        self.dataset_pokemons = dataset.get_all_pokemons()
        self.dataset_movements = dataset.get_all_movements()
        self.type_matrix = dataset.get_types_matrix()

    def run_single_experiment(self, def_team_experiment: str, n_ants=10, alpha=0.5, beta=1.0, rho=0.75, n_cicles_no_improve=50) -> pd.DataFrame:
        """
        Runs an experiment with the given ACO algorithm and dataset.
        """

        def_team = self._read_data(def_team_experiment)
        
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
    
    def run_repeated_experiment(self, experiment_id: int, n_repeat=31, n_ants=10, alpha=0.5, beta=1.0, rho=0.75, n_cicles_no_improve=50) -> pd.DataFrame:
        """
        Runs an experiment with the given ACO algorithm and dataset n_repeat times.
        Returns a DataFrame with the fitness and number of cicles of each run.
        results = [] 
        for i in range(n_repeat):
            print(f"Running experiment: dataset {experiment_id} - run {i+1}/{n_repeat}")
            aco = self.run_single_experiment(experiment_id, n_ants, alpha, beta, rho, n_cicles_no_improve)
            actual_result = {
                "run": i,
                "fitness": 1.0/aco.best_fitness,
                "n_evaluations": aco.n_evaluations
            }
            results.append(actual_result)

        return pd.DataFrame(results)
        """ 
        pass
    
    def run_all_experiments(self, experiment_folder: str, overwrite=False, n_repeat=31):
        """
        Runs all experiments in the dataset n_repeat times.
        Returns a DataFrame with the fitness and number of cicles of each run.
        """
        pass

    def _read_data(self, def_team_experiment: int):
        
        data = self.dataset.query(f"id == {def_team_experiment}").iloc[0]

        if len(data) == 0:
            raise ValueError(f"Experiment with id {def_team_experiment} not found.")

        n_blades = data["N"]
        times = {
            "Zu": {
                "F": data["forging_zubora"],
                "G": data["grinding_zubora"]
            },
            "Ga": {
                "F": data["forging_gabora"],
                "G": data["grinding_gabora"]
            }
        }
        return n_blades, times
    
    def _calculate_params(self, experiment_id: int) -> Dict[str, float]:
        """
        Calculates the parameters for the ACO algorithm based on the dataset.
        """
        fixed = {
            "alpha": 0.5,
            "beta": 1.0,
            "rho": 0.75,
            "n_cicles_no_improve": 50
        }

        data = self.dataset.query(f"id == {experiment_id}").iloc[0]
        if data["N"] < 100:
            fixed["n_ants"] = 10
        elif data["N"] < 1000:
            fixed["n_ants"] = 50
        else:
            fixed["n_ants"] = 100

        return fixed