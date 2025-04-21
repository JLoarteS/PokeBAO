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
        return isinstance(other, Move) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

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
        # Auxiliar list of moves without previously selected moves
        aux = [m for m in self.moves if m not in [self.move1, self.move2, self.move3, self.move4]]
        
        if len(aux) > 0:
            return aux[random.randrange(len(aux))]
        else:
            return None
    
    def STAB(self, move : Move) -> float:
        if self.type1 == move.type or self.type2 == move.type:
            return 1.5
        else:
            return 1
    
    def damage_calculation(self, poke_defender) -> float:
        def fun_damage(move : Move, defender : Pokemon):
            from dataset import get_types_matrix
            LEVEL = 100
            CRITICAL = 1
            RANDOM = 1

            if move is None:
                return 0

            type_matrix = get_types_matrix()

            type1_effectiveness = type_matrix[defender.type1][move.type]
            type2_effectiveness = type_matrix[defender.type2][move.type] if defender.type2 is not None else 1
            
            base = (((2 * LEVEL * CRITICAL / 5 + 2) * move.power * self.attack / defender.defense) / 50) + 2
            return (base * self.STAB(move) * type1_effectiveness * type2_effectiveness * RANDOM * (move.accuracy / 100))
        
        damage1 = fun_damage(self.move1, poke_defender)
        damage2 = fun_damage(self.move2, poke_defender)
        damage3 = fun_damage(self.move3, poke_defender)
        damage4 = fun_damage(self.move4, poke_defender)
        
        return damage1 + damage2 + damage3 + damage4
    
    def __str__(self) -> str:
        return self.name
    
    
def damage_calculation(poke_attacker : Pokemon, poke_defender : Pokemon):
    def fun_damage(attacker : Pokemon, move : Move, defender : Pokemon):
        from dataset import get_types_matrix
        LEVEL = 100
        CRITICAL = 1
        RANDOM = 1

        if move is None:
            return 0

        type_matrix = get_types_matrix()

        type1_effectiveness = type_matrix[defender.type1][move.type]
        type2_effectiveness = type_matrix[defender.type2][move.type] if defender.type2 is not None else 1
        accuracy = move.accuracy if move.accuracy is not None else 100
        
        base = (((2 * LEVEL * CRITICAL / 5 + 2) * move.power * attacker.attack / defender.defense) / 50) + 2
        return (base * attacker.STAB(move) * type1_effectiveness * type2_effectiveness * RANDOM * (accuracy / 100))
    
    damage1 = fun_damage(poke_attacker, poke_attacker.move1, poke_defender)
    damage2 = fun_damage(poke_attacker, poke_attacker.move2, poke_defender)
    damage3 = fun_damage(poke_attacker, poke_attacker.move3, poke_defender)
    damage4 = fun_damage(poke_attacker, poke_attacker.move4, poke_defender)
    
    return damage1 + damage2 + damage3 + damage4