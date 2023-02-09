from battleship.model.battlefield import Battlefield
from battleship.representation.battlefield_representation import BattlefieldRepresentation


class PlaceShipsRepresentation:

    def __init__(self, battlefield: Battlefield, ships_left: dict):
        self._battlefield = battlefield
        self._ships_left = ships_left

    def get_representation(self, console_width: int) -> str:
        ships_count_representation = "Ships left:\n"
        for i in range(1, len(self._ships_left)):
            ships_count_representation += f"{i}: {self._ships_left.get(i, 0)} left\n"
            
        delimiter = "===================\nCURRENT BATTLEFIELD\n===================\n"
        
        battlefield_representation = BattlefieldRepresentation(self._battlefield).get_representation(console_width)
        
        return ships_count_representation + delimiter + battlefield_representation

