from functools import reduce
from typing import Optional

from battleship.model.battlefield import Battlefield


class BattlefieldRepresentation:
    _battlefield: Battlefield

    _VERTICAL_AXIS_LABELS_LENGTH = 3

    def __init__(self, battlefield: Battlefield):
        self._battlefield = battlefield
        self._ships_coordinates = reduce(
            lambda a, b: a.union(b),
            [set(s.coordinates) for s in self._battlefield.ships],
            set()
        )

    def get_representation(self, console_width: int) -> str:
        result = ""
        if console_width <= BattlefieldRepresentation._VERTICAL_AXIS_LABELS_LENGTH:
            raise Exception("Not enough space to display the game")

        offset = 0
        while offset < self._battlefield.plane.size[0]:
            width = min(console_width - self._VERTICAL_AXIS_LABELS_LENGTH, self._battlefield.plane.size[0] - offset)
            result += self._represent_slice_of_battlefield(offset, width) + "\n"
            offset += width

        return result

    def _represent_header(self, offset: Optional[int] = None, width: Optional[int] = None) -> str:
        result = " " * self._VERTICAL_AXIS_LABELS_LENGTH
        offset = offset or 0
        width = width or self._battlefield.plane.size[0]
        return result + "".join(
            self._battlefield.plane.from_local_coordinates((offset + i, 0))[0]
            for i in range(width)
        )

    def _represent_slice_of_battlefield(self, offset: int, width: int) -> str:
        result = self._represent_header(offset, width)
        result += "\n" + "".join("-" if c != " " else " " for c in result) + "\n"
        return result + "\n".join(
            "{0: >2}|".format(self._battlefield.plane.from_local_coordinates((0, y))[1]) +
            "".join("S" if self._battlefield.plane.from_local_coordinates((x, y)) in self._ships_coordinates else " "
                    for x in range(width))
            for y in range(self._battlefield.plane.size[1])
        )
