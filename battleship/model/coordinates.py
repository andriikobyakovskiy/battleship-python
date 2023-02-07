from typing import Tuple, Union, List
from dataclasses import dataclass

from battleship.model.exceptions import CoordinatesTypeException

Coordinate = Union[int, str]
Coordinates = Tuple[Coordinate, Coordinate]


def coordinate_without_offset(target: Coordinate, offset: Coordinate) -> int:
    if type(target) is not type(offset):
        raise CoordinatesTypeException(
            f"Cannot adjust target coordinate of type {type(target)} with {type(offset)} offset."
        )

    return ord(target) - ord(offset) if type(offset) is str else target - offset


def coordinate_with_offset(target: int, offset: Coordinate) -> Coordinate:
    return chr(target + ord(offset)) if type(offset) is str else target + offset


@dataclass(frozen=True)
class Plane:
    size: Tuple[int, int]
    offset: Coordinates = (0, 0)

    def contains(self, target: Coordinates) -> bool:
        return all(
            0 <= coordinate_without_offset(coordinate, offset) < dimension
            for coordinate, offset, dimension
            in zip(target, self.offset, self.size)
        )

    def __contains__(self, target: Coordinates) -> bool:
        return self.contains(target)

    @property
    def coordinates(self) -> List[Coordinates]:
        return [
            (
                coordinate_with_offset(x, self.offset[0]),
                coordinate_with_offset(y, self.offset[1]),
            )
            for y in range(self.size[1])
            for x in range(self.size[0])
        ]

    def to_local_coordinates(self, target: Coordinates) -> Tuple[int, int]:
        return tuple((
            coordinate_without_offset(coord, offset)
            for coord, offset in zip(target, self.offset)
        ))

    def from_local_coordinates(self, target: Tuple[int, int]) -> Coordinates:
        return tuple((
            coordinate_with_offset(coord, offset)
            for coord, offset in zip(target, self.offset)
        ))
