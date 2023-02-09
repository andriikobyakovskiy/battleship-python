from dataclasses import dataclass
from typing import Dict, Optional
import re

from battleship.activity.single_player_loop import SinglePlayerLoop
from battleship.model.battlefield import Battlefield, Ship
from battleship.model.exceptions import CoordinatesValueException
from battleship.representation.place_ships_representation import PlaceShipsRepresentation


class PlacementResult:
    pass


@dataclass
class Error(PlacementResult):
    message: str


class Success(PlacementResult):
    pass


class Ready(PlacementResult):
    pass


class PlaceShipsLoop(SinglePlayerLoop[PlacementResult]):

    def __init__(self, battlefield: Battlefield, ships_count: Dict[int, int]):
        self.battlefield = battlefield
        self._ships_count = ships_count.copy()
        self._add_ship_regexp = re.compile(r"(?P<x>[A-Ja-j])(?P<y>[1-9]|10)(?P<orientation>[HhVv])(?P<length>[1-5])")
        self._remove_ship_regexp = re.compile(r"(?P<x>[A-Ja-j])(?P<y>[1-9]|10)")

    @property
    def ships_left(self):
        return self._ships_count.copy()

    def run_iteration(self, console_width: int) -> PlacementResult:
        print(PlaceShipsRepresentation(self.battlefield, self.ships_left).get_representation(console_width))
        if self.all_ships_placed():
            final_input = input((
                "Enter any ship coordinate to remove it (for example 'A1')\n"
                "OR\n"
                "Enter 'ready' to submit ships positions\n"
                ">>> "
            ))
            match_remove = self._remove_ship_regexp.match(final_input)
            if match_remove:
                return self._try_remove(**match_remove.groupdict())

            if final_input.strip() == 'ready':
                return Ready()

            return Error("Cannot parse command " + final_input)

        ship_input = input((
            "Enter any ship coordinate to remove it (for example 'A1')\n"
            "OR\n"
            "To add ship enter start coordinates, orientation (H or V) and ship length (for example 'A1H3')\n"
            ">>> "
        ))
        match_add = self._add_ship_regexp.match(ship_input)
        if match_add:
            if self._ships_count[int(match_add.group("length"))] <= 0:
                return Error(f"No ships of length {match_add.group('length')} left")
            return self._try_add(**match_add.groupdict())

        match_remove = self._remove_ship_regexp.match(ship_input)
        if match_remove:
            return self._try_remove(**match_remove.groupdict())

        return Error("Input doesn't match add or remove ship instructions")

    def _try_add(self, x, y, orientation, length):
        try:
            length = int(length)
            self.battlefield.add_ship(Ship(
                (x.upper(), int(y)),
                Ship.Orientation(orientation.upper()),
                length
            ))
            self._ships_count[length] -= 1
            return Success()
        except CoordinatesValueException as e:
            return Error(e.args[0])

    def _try_remove(self, x, y):
        result = self.battlefield.remove_ship((x.upper(), int(y)))
        if result:
            self._ships_count[result.length] += 1
            return Success()

        return Error("Ship not found at these coordinates")

    def turn_end_check(self, event_object: PlacementResult) -> bool:
        return event_object is not None and isinstance(event_object, Ready)

    def get_error_from_result(self, event_object: PlacementResult) -> Optional[str]:
        return event_object.message if event_object is not None and isinstance(event_object, Error) else None

    def get_activity_result(self) -> object:
        return self.battlefield

    def all_ships_placed(self) -> bool:
        return all((cnt == 0 for cnt in self._ships_count.values()))
