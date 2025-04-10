import pokebase as pb
import json

from data.dataset import get_types_matrix

class Move:
    def __init__(self, name = None):
        self.name = name
        
        self.power = None
        self.type = None
        self.accuracy = None

        if name is not None:
            with open("movements.json", "r") as f:
                movements = json.load(f)
            self.power = movements[name]["power"]
            self.type = movements[name]["type"]
            self.accuracy = movements[name]["accuracy"]

class Pokemon:
    # id ; nombre ; tipo1 ; tipo2 ; ataque ; defensa ; move1,2,3,4
    def __init__(self, id):
        self.id = id
        with open("pokemons.json", "r") as f:
            poke = json.load(f)
        self.name = poke[str(id)]["name"]
        self.type1 = poke[str(id)]["types"][0]
        if(len(poke[str(id)]["types"]) == 2):
            self.type2 = poke[str(id)]["types"][1]
        else:
            self.type2 = "joker"
        self.attack = poke[str(id)]["attack"]
        self.defense = poke[str(id)]["defense"]
        self.movementList = poke[str(id)]["moves"]
        self.move1 = Move()
        self.move2 = Move()
        self.move3 = Move()
        self.move4 = Move()

def damage_calculation(poke_attacker:Pokemon, poke_defender:Pokemon):
    LEVEL = 100
    CRITICAL = 1
    RANDOM = 100

    def fun_damage(attacker, move, defender):
        LEVEL = 100
        CRITICAL = 1
        RANDOM = 100

        if move.name == None:
            return 0
        
        
        base = (((2 * LEVEL * CRITICAL / 5 + 2) * move.power * poke_attacker.attack / poke_defender.defense) / 50)
        return ((base + 2) * stab(poke_attacker, move) * get_types_matrix()[defender.type1][move.type] * get_types_matrix()[defender.type2][move.type] * RANDOM * (move.accuracy/100))

    def stab(poke:Pokemon, move:Move):
        ret = 1
        if((poke.type1 == move.type) | (poke.type2 == move.type)):
            ret = 1.5
        else:
            ret = 1
        return ret
        

    damage1 = fun_damage(poke_attacker, poke_attacker.move1, poke_defender)
    damage2 = fun_damage(poke_attacker, poke_attacker.move2, poke_defender)
    damage3 = fun_damage(poke_attacker, poke_attacker.move3, poke_defender)
    damage4 = fun_damage(poke_attacker, poke_attacker.move4, poke_defender)
    
    return damage1 + damage2 + damage3 + damage4
    