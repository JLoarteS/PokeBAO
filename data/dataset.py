import json
import pandas as pd

from data.pokemon import Pokemon, Move

def get_all_pokemons(random_moves: bool = False) -> list[Pokemon]:
    # JSON with pokemons
    with open("data/pokemons.json", "r") as f:
        pokemons_json = json.load(f)
    
    pokemons = []
    
    for id in pokemons_json:
        name = pokemons_json[id]["name"]
        
        pokemons.append(get_pokemon(id, name, random_moves, pokemons_json))
    
    return pokemons

def get_pokemon(id: str, name: str, random_moves: bool = False, data_json: dict | None = None) -> Pokemon:
    
    if data_json is None:
        # JSON with pokemons
        with open("data/pokemons.json", "r") as f:
            pokemons_json = json.load(f)
    else:
        pokemons_json = data_json
    
    pokemon_data = next((pokemon for pokemon in pokemons_json.values() if pokemon["name"] == name), None)
    
    if pokemon_data is None:
        return None
    
    movements = get_all_movements()
    
    type1 = pokemon_data["types"][0]
    type2 = pokemon_data["types"][1] if len(pokemon_data["types"]) > 1 else "joker"
    attack = pokemon_data["attack"]
    defense = pokemon_data["defense"]
    moves = pokemon_data["moves"]
    
    moves_list = []
    for move in movements:
        if move in moves:
            moves_list.append(move)
    
    return Pokemon(int(id), name, type1, attack, defense, moves_list, type2, random_moves)

def get_all_movements() -> list[Move]:
    # JSON with movements
    with open("data/movements.json", "r") as f:
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
    with open("data/types.json", "r") as f:
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
# print(get_pokemon("bulbasaur"))
# print(get_all_movements())
# print(get_types_matrix())