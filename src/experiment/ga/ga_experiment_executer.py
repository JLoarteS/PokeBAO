import pandas as pd
from os import makedirs
from os.path import isdir
import random

from src.ga.ga_pokebao import GAPokebao
import data.dataset as dataset
from data.pokemon import Pokemon

class GAExperimentExecuter:
    
    def __init__(self, max_evaluations: int = 100):
        self.max_evaluations = max_evaluations

        self.experiments = pd.read_csv('data/experiment/experiments.csv')
        self.data_def_teams = pd.read_csv(f"data/experiment/def_teams.csv")
        
        self.dataset_pokemons = dataset.get_all_pokemons()
        self.dataset_movements = dataset.get_all_movements()
        self.type_matrix = dataset.get_types_matrix()

    def run_single_experiment(self, def_team_experiment: str = 'all', num_teams_def=6, **kwargs) -> pd.DataFrame:
        """
        Runs an experiment with the given GA algorithm and dataset.
        Returns the best solution find in the experiment.
        """
        def_team = self._read_defenders_data(def_team_experiment, num_teams_def)
        
        ga = GAPokebao(
            def_team=def_team,
            all_pokemons=self.dataset_pokemons,
            **kwargs
        )
        ga.run(self.max_evaluations)
        candidate, fitness = ga.run()
        return ga, candidate, fitness
    
    def run_repeated_experiment(self, def_team_experiment: str = 'all', num_teams_def=6, n_repeat=31, **kwargs) -> pd.DataFrame:
        """
        Runs an experiment with the given GA algorithm and dataset n_repeat times.
        Returns a DataFrame with the fitness and number of cicles of each run.
        """
        results = []
        for i in range(n_repeat):
            print(f"Running experiment: dataset {def_team_experiment} - run {i+1}/{n_repeat}")
            ga, candidate, fitness = self.run_single_experiment(def_team_experiment, num_teams_def, **kwargs)
            actual_result = {
                "run": i,
                "fitness": fitness,
                "n_evaluations": ga.num_evaluations
            }
            results.append(actual_result)

        return pd.DataFrame(results)
    
    def run_all_experiments(self, n_repeat=31, experiments=[]):
        """
        Runs all experiments in the dataset n_repeat times.
        """
        experiment_folder = 'experiments/ga'

        if not isdir(experiment_folder):
            makedirs(experiment_folder)

        for i in self.experiments['id'].to_list():
            if experiments != [] and i not in experiments:
                continue

            def_team_experiment = self.experiments.query(f"id == {i}")['source_team'].iloc[0]
            num_teams_def = self.experiments.query(f"id == {i}")['num_teams_def'].iloc[0]

            print(f"Running experiment {i}")
            actual_result = self.run_repeated_experiment(
                def_team_experiment,
                num_teams_def=num_teams_def,
                n_repeat=n_repeat
            )

            actual_result["experiment_id"] = i
            actual_result.to_csv(f"{experiment_folder}/experiment_{i}.csv", index=False)
            print(f"Experiment {i} finished and saved.")

    def _read_defenders_data(self, def_team_experiment, num_leaders: int = 6) -> list[Pokemon]:
        """
        Returns a list of pre-made teams of defenders.
        """
        def_team = []
        data_leaders = []
        
        # Read CSV
        if def_team_experiment != "all":
            data_leaders = self.data_def_teams.query(f"source == '{def_team_experiment}'").groupby(['source', 'id_leader'])['pokemon'].apply(list).to_list()
        else:
            data_leaders = self.data_def_teams.groupby(['source', 'id_leader'])['pokemon'].apply(list).to_list()
        
        # Shuffle the leaders to randomize the experiments
        random.shuffle(data_leaders)
        
        # Concat all the pokemons names from all chosen leaders
        pokemons_names = [pokemon for leaders in data_leaders[:num_leaders] for pokemon in leaders]
        print('Def team:', pokemons_names)
        
        # Create a list with Pokemon object from the leaders' pokemons
        def_team = []

        # Find the Pokemon object from the all_pokemons data
        for name in pokemons_names:
            for pokemon in self.dataset_pokemons:
                if pokemon.name == name:
                    def_team.append(pokemon)
                    break
        
        return def_team