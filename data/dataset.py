import json
import pandas as pd

from pokemon import Pokemon, Move

def get_all_pokemons(random_moves : bool = False):
    # JSON with pokemons
    with open("pokemons.json", "r") as f:
        pokemons_json = json.load(f)
    
    pokemons = []
    
    movements = get_all_movements()
    
    for id in pokemons_json:
        name = pokemons_json[id]["name"]
        type1 = pokemons_json[id]["types"][0]
        type2 = pokemons_json[id]["types"][1] if len(pokemons_json[id]["types"]) > 1 else "joker"
        attack = pokemons_json[id]["attack"]
        defense = pokemons_json[id]["defense"]
        moves = pokemons_json[id]["moves"]
        
        movesList = []
        for move in moves:
            for m in movements:
                if move == str(m):
                    movesList.append(m)
                
        pokemons.append(Pokemon(id, name, type1, attack, defense, movesList, type2, random_moves))
    
    return pokemons

def get_all_movements():
    # JSON with movements
    with open("movements.json", "r") as f:
        movements_json = json.load(f)
    
    movements = []
    
    for name in movements_json:
        id = movements_json[name]["id"]
        power = movements_json[name]["power"]
        type = movements_json[name]["type"]
        accuracy = movements_json[name]["accuracy"]
        
        movements.append(Move(name, id, power, type, accuracy))
    
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

# print(get_all_pokemons())
# print(get_all_movements())
# print(get_types_matrix())