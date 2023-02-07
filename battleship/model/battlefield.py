from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from battleship.model.coordinates import Coordinates, Plane, coordinate_with_offset
from battleship.model.exceptions import CoordinatesValueException


@dataclass(frozen=True)
class Ship:

    class Orientation(Enum):
        HORIZONTAL = 'H'
        VERTICAL = 'V'

    position: Coordinates
    orientation: Orientation
    length: int

    @property
    def coordinates(self) -> List[Coordinates]:
        offset_x, offset_y = self.position
        return [
            (coordinate_with_offset(i, offset_x), offset_y)
            if self.orientation == Ship.Orientation.HORIZONTAL
            else (offset_x, coordinate_with_offset(i, offset_y))
            for i in range(self.length)
        ]


class Battlefield:
    plane: Plane
    ships: List[Ship]

    def __init__(self, plane: Plane, ships: Optional[List[Ship]] = None):
        self.plane = plane
        self.ships = ships.copy() if ships else list()

    def add_ship(self, ship: Ship):
        for c in ship.coordinates:
            if c not in self.plane:
                raise CoordinatesValueException(
                    f"Coordinates {c} of ship {ship} do not fit in field {self.plane}"
                )
            for s in self.ships:
                if c in s.coordinates:
                    raise CoordinatesValueException(
                        f"Coordinates {c} of ship {ship} intersects with existing ship {s}"
                    )

        self.ships.append(ship)
