from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class Battlefield:
    plane: Plane
    ships: List[Ship] = field(default_factory=list)

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

    def remove_ship(self, target: Coordinates) -> Optional[Ship]:
        print([s.coordinates for s in self.ships])
        ships_to_remove = [s for s in self.ships if target in s.coordinates]
        if not ships_to_remove:
            return None

        result = ships_to_remove[0]
        self.ships.remove(result)
        return result
