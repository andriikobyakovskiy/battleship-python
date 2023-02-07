import unittest

from battleship.model.coordinates import Plane
from battleship.model.exceptions import CoordinatesTypeException


class TestCoordinates(unittest.TestCase):

    def setUp(self) -> None:
        self.planeOffsets = ('A', 1)
        self.planeSize = (3, 3)
        self.simplePlane = Plane(self.planeSize, self.planeOffsets)

    def test_contains(self):
        self.assertTrue(('A', 1) in self.simplePlane)
        self.assertTrue(('A', 3) in self.simplePlane)
        self.assertTrue(('C', 1) in self.simplePlane)
        self.assertTrue(('C', 3) in self.simplePlane)
        self.assertTrue(('B', 2) in self.simplePlane)

        self.assertFalse(('A', 10) in self.simplePlane)
        self.assertFalse(('F', 1) in self.simplePlane)
        with self.assertRaises(CoordinatesTypeException):
            self.simplePlane.contains((1, 1))

    def test_coordinates_generation(self):
        self.assertEqual(
            set(self.simplePlane.coordinates),
            {
                ('A', 1), ('A', 2), ('A', 3),
                ('B', 1), ('B', 2), ('B', 3),
                ('C', 1), ('C', 2), ('C', 3),
            }
        )

    def test_to_local_coordinates(self):
        self.assertEqual(self.simplePlane.to_local_coordinates(('A', 1)), (0, 0))
        self.assertEqual(self.simplePlane.to_local_coordinates(('C', 3)), (2, 2))
        self.assertEqual(self.simplePlane.to_local_coordinates(('A', 3)), (0, 2))
