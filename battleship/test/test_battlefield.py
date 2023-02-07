import unittest

from battleship.model.coordinates import Plane
from battleship.model.exceptions import CoordinatesValueException
from battleship.model.battlefield import Ship, Battlefield


class TestBattlefield(unittest.TestCase):
    battlefield: Battlefield

    def setUp(self) -> None:
        self.planeOffsets = ('A', 1)
        self.planeSize = (3, 3)
        self.simplePlane = Plane(self.planeSize, self.planeOffsets)

    @staticmethod
    def with_new_battlefield(method):
        def _wrapped_method(self):
            self.battlefield = Battlefield(self.simplePlane)
            method(self)
        return _wrapped_method

    @with_new_battlefield
    def test_ships_intersection(self):
        self.battlefield.add_ship(Ship(('A', 2), Ship.Orientation.HORIZONTAL, 3))
        with self.assertRaises(CoordinatesValueException):
            self.battlefield.add_ship(Ship(('B', 1), Ship.Orientation.VERTICAL, 3))

    @with_new_battlefield
    def test_ships_out_of_battlefield(self):
        with self.assertRaises(CoordinatesValueException):
            self.battlefield.add_ship(Ship(('B', 1), Ship.Orientation.VERTICAL, 4))

    @with_new_battlefield
    def test_correct_ships_placement(self):
        self.battlefield.add_ship(Ship(('A', 1), Ship.Orientation.VERTICAL, 3))
        self.battlefield.add_ship(Ship(('C', 1), Ship.Orientation.VERTICAL, 3))
        self.assertEqual(
            [ s.coordinates for s in self.battlefield.ships ],
            [
                [('A', 1), ('A', 2), ('A', 3)],
                [('C', 1), ('C', 2), ('C', 3)],
            ]
        )

    def test_ship_coordinates(self):
        ship = Ship(('A', 1), Ship.Orientation.HORIZONTAL, 2)
        self.assertEqual(set(ship.coordinates), {('A', 1), ('B', 1)})

