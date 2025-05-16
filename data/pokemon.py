import random

class Move:
    # name ; id_pokedex ; power ; type ; accuaracy
    def __init__(self, name: str, id_pokedex: int, power: int, type: str, accuracy: int):
        self.name = name
        self.id_pokedex = id_pokedex
        self.power = power
        self.type = type
        self.accuracy = accuracy
    
    def type_effectiveness(self, def_type1: str, def_type2: str | None):
        """
        Calculates the effectiveness of type to a pokemon
        """
        from data.dataset import get_types_matrix
        type_matrix = get_types_matrix()

        type1_effectiveness = type_matrix[def_type1][self.type]
        type2_effectiveness = type_matrix[def_type2][self.type] if def_type2 is not None else 1
        
        return type1_effectiveness * type2_effectiveness

    def __eq__(self, other) -> bool:
        return (isinstance(other, Move) and self.name == other.name) or (isinstance(other, str) and self.name == other)
    
    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

class Pokemon:
    # id_pokedex ; name ; type1; attack ; defense ; move_list ; type2 ; random_moves
    def __init__(self, id_pokedex: int, name: str, type1: str, attack: int, defense: int, moves_list: list[Move], type2: str = "joker", random_moves: bool = False):
        self.id_pokedex = id_pokedex
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.attack = attack
        self.special_attack = attack
        self.defense = defense
        self.special_defense = defense
        self.all_moves = moves_list # list of Move objects with all movements
        self.moves = []
        
        if random_moves:
            self.set_all_random_moves()
    
    def set_all_random_moves(self):
        """
        Set all moves with random moves
        """
        self.moves = []
        
        for _ in range(4):
            self.moves.append(self.get_random_move())        
    
    def get_random_move(self) -> Move | None:
        """
        Get a random move from self.all_moves
        """
        
        # Auxiliar list of moves without previously selected moves
        aux = [m for m in self.all_moves if m not in self.moves]
        
        if len(aux) > 0:
            return aux[random.randrange(len(aux))]
        else:
            return None
    
    def add_move(self, name: str) -> bool:
        """
        Add a move to self.moves
        """
        if name in self.all_moves and len(self.moves) < 4:
            self.moves.append(self.all_moves[self.all_moves.index(name)])
            return True
        else:
            return False
    
    def remove_move(self, name: str) -> bool:
        """
        Remove a move from moves
        """
        if name in self.moves:
            self.moves.remove(name)
            return True
        else:
            return False
    
    def change_move(self, move_old: Move | str, move_new: Move | str):
        """
        Change two moves, remove an old move and add a new move
        """
        if move_old not in self.moves:
            return False
        
        self.remove_move(move_old)
        
        self.add_move(move_new)
    
    def STAB(self, move: Move) -> float:
        """
        Calculate the STAB (Same-Type Attack Bonus)
        """
        if self.type1 == move.type or self.type2 == move.type:
            return 1.5
        else:
            return 1
    
    def damage_calculation(self, poke_defender) -> float:
        """
        Calculates the damage it does to a pokemon
        """
        def fun_damage(move: Move, defender: Pokemon):
            from data.dataset import get_types_matrix
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
        
        damage = 0
        for move in self.moves:
            damage += fun_damage(move, poke_defender)
        
        return damage
    
    def get_str_moves(self) -> str:
        return ', '.join([move.name for move in self.moves])

    def __eq__(self, other) -> bool:
        return (isinstance(other, Pokemon) and self.name == other.name) or (isinstance(other, str) and self.name == other)
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name + ": " + self.get_str_moves()

def damage_calculation_pokemon(poke_attacker: Pokemon, poke_defender: Pokemon):
    """
    Calculates damage
    """
    return poke_attacker.damage_calculation(poke_defender)

def type_effectiveness_move(move: Move, poke_defender: Pokemon):
    """
    Calculates type effectiveness
    """
    return move.type_effectiveness(poke_defender.type1, poke_defender.type2)