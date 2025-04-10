import random

class Move:
    # name ; id ; power ; type ; accuaracy
    def __init__(self, name : str, id : int, power : int, type : str, accuracy : int):
        self.name = name
        self.id = id
        self.power = power
        self.type = type
        self.accuracy = accuracy
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.name == self.name and self.id == self.id
        return False

    def __str__(self) -> str:
        return self.name

class Pokemon:
    # id ; name ; type1 ; type2 ; attack ; defense ; moveList ; move1,2,3,4
    def __init__(self, id : int, name : str, type1 : str, attack : int, defense : int, moves : list, type2 : str = "joker", random_moves : bool = False):
        self.id = id
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.attack = attack
        self.special_attack = attack
        self.defense = defense
        self.special_defense = defense
        self.moves = moves
        self.move1 = None
        self.move2 = None
        self.move3 = None
        self.move4 = None
        
        if random_moves:
            self.move1 = self.get_random_move()
            self.move2 = self.get_random_move()
            self.move3 = self.get_random_move()
            self.move4 = self.get_random_move()
    
    def get_random_move(self) -> Move:
        
        # Auxiliar list of movements
        aux = self.moves.copy()
        if self.move1 in aux:
            aux.remove(self.move1)
        if self.move2 in aux:
            aux.remove(self.move1)
        if self.move3 in aux:
            aux.remove(self.move1)
        if self.move4 in aux:
            aux.remove(self.move1)
        
        if len(aux) > 0:
            las = random.choice(aux)
            print(las, type(las))
            return las
        else:
            return None
    
    def STAB(self, move) -> float:
        ret = 1
        if((self.type1 == move.type) | (self.type2 == move.type)):
            ret = 1.5
        else:
            ret = 1
        return ret
    
    def __str__(self) -> str:
        return self.name
    
    
def damage_calculation(poke_attacker : Pokemon, poke_defender : Pokemon):
    def fun_damage(attacker : Pokemon, move : Move, defender : Pokemon):
        from dataset import get_types_matrix
        
        LEVEL = 100
        CRITICAL = 1
        RANDOM = 100
        
        print(move)

        if move is None:
            return 0
        
        base = (((2 * LEVEL * CRITICAL / 5 + 2) * move.power * attacker.attack / defender.defense) / 50)
        return ((base + 2) * attacker.STAB(move) * get_types_matrix()[defender.type1][move.type] * get_types_matrix()[defender.type2][move.type] * RANDOM * (move.accuracy / 100))
        

    damage1 = fun_damage(poke_attacker, poke_attacker.move1, poke_defender)
    damage2 = fun_damage(poke_attacker, poke_attacker.move2, poke_defender)
    damage3 = fun_damage(poke_attacker, poke_attacker.move3, poke_defender)
    damage4 = fun_damage(poke_attacker, poke_attacker.move4, poke_defender)
    
    return damage1 + damage2 + damage3 + damage4