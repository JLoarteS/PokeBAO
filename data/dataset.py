import json
import pandas as pd

def get_all_pokemons():
    # JSON with pokemons
    with open("pokemons.json", "r") as f:
        pokemons = json.load(f)
    
    return pokemons

def get_all_movements():
    # JSON with movements
    with open("movements.json", "r") as f:
        movements = json.load(f)
    
    return movements

def get_types_matrix():
    # JSON with types
    with open("types.json", "r") as f:
        types = json.load(f)

    matrix = pd.DataFrame(1.0, index=[t["name"] for t in types], columns=[t["name"] for t in types])
    
    for t in types:
        attacker = t["name"]
        for defender in t["strengths"]:
            matrix.at[attacker, defender] = 2.0
        for defender in t["weaknesses"]:
            matrix.at[attacker, defender] = 0.5
        for defender in t["immunes"]:
            matrix.at[attacker, defender] = 0.0
    
    return matrix

# Test

# get_all_pokemons()
# get_all_movements()
# get_types_matrix()