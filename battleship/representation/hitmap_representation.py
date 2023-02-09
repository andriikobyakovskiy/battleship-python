from __future__ import annotations
from typing import List, Tuple, Optional

from battleship.model.battlelog import Hitmap, HitmapCell
from battleship.model.exceptions import CoordinatesValueException


class HitmapRepresentation:
    DoShowShips = bool
    _hitmaps: List[Tuple[Hitmap, DoShowShips]]

    _VERTICAL_AXIS_LABELS_LENGTH = 2

    def __init__(self, battlefield: Hitmap, show_ships: bool = False):
        self._hitmaps = [(battlefield, show_ships)]

    def __add__(self, other: HitmapRepresentation) -> HitmapRepresentation:
        if any(hm.battlefield.plane.size != self._hitmaps[0][0].battlefield.plane.size for hm, _ in other._hitmaps):
            raise CoordinatesValueException("Cannot represent in one view hitmaps for battlefields of different size")

        self._hitmaps.extend(other._hitmaps)
        return self

    def get_representation(self, console_width: int, tab_size: int = 3) -> str:
        current_used_space = 0
        current_hitmaps = []
        result = ""
        if console_width <= HitmapRepresentation._VERTICAL_AXIS_LABELS_LENGTH:
            raise Exception("Not enough space to display the game")

        for hm, show_ships in self._hitmaps:
            # if a single battlefield doesn't fit console split it and show as much as possible on one line
            if current_used_space == 0 and hm.battlefield.plane.size[0] > console_width:
                offset = 0
                while offset < hm.battlefield.plane.size[0]:
                    width = min(
                        console_width - self._VERTICAL_AXIS_LABELS_LENGTH,
                        hm.battlefield.plane.size[0] - offset
                    )
                    result += self._represent_header(hm, offset, width) + "\n"
                    result += self._represent_slice_of_hitmap(hm, show_ships, offset, width) + "\n"
                    offset += width

                return result
            # if we already have a hitmap and try to insert one more, but it doesn't fit - put it on the next line
            else:
                if current_used_space + hm.battlefield.plane.size[0] > console_width:
                    result += HitmapRepresentation._represent_hitmaps(current_hitmaps, tab_size)
                    current_used_space = 0
                    current_hitmaps.clear()

                current_hitmaps.append((hm, show_ships))
                current_used_space += hm.battlefield.plane.size[0]

        result += HitmapRepresentation._represent_hitmaps(current_hitmaps, tab_size)
        return result

    @staticmethod
    def _represent_cell(cell: HitmapCell, show_ships: bool):
        if cell.was_hit and cell.contents is None:
            return "O"
        if cell.was_hit and cell.contents is not None:
            return "X"
        if cell.contents is not None and show_ships:
            return "S"
        return " "

    @staticmethod
    def _represent_header(hitmap: Hitmap, offset: Optional[int] = None, width: Optional[int] = None) -> str:
        result = " " * HitmapRepresentation._VERTICAL_AXIS_LABELS_LENGTH
        offset = offset or 0
        width = width or hitmap.battlefield.plane.size[0]
        return result + "".join(
            hitmap.battlefield.plane.from_local_coordinates((offset + i, 0))[0]
            for i in range(width)
        )

    @staticmethod
    def _represent_row(
        hitmap: Hitmap,
        y: int,
        show_ships: bool,
        offset: Optional[int] = None,
        width: Optional[int] = None,
    ) -> str:
        result = "{}|".format(hitmap.battlefield.plane.from_local_coordinates((0, y))[1])
        offset = offset or 0
        width = width or hitmap.battlefield.plane.size[0]
        return result + "".join(
            HitmapRepresentation._represent_cell(hitmap.map[offset + i][y], show_ships)
            for i in range(width)
        )

    @staticmethod
    def _represent_slice_of_hitmap(hitmap: Hitmap, show_ships: bool, offset: int, width: int) -> str:
        result = HitmapRepresentation._represent_header(hitmap, offset, width)
        result += "\n" + "".join("-" if c != " " else " " for c in result) + "\n"
        return result + "\n".join(
            HitmapRepresentation._represent_row(hitmap, y, show_ships)
            for y in range(hitmap.battlefield.plane.size[1])
        )

    @staticmethod
    def _represent_hitmaps(hitmaps: List[Tuple[Hitmap, DoShowShips]], tab_size: int) -> str:
        tab = " " * tab_size
        result = tab.join(
            HitmapRepresentation._represent_header(hm)
            for hm, _ in hitmaps
        )
        result += "\n" + "".join("-" if c != " " else " " for c in result) + "\n"
        return result + "\n".join(
            tab.join(
                HitmapRepresentation._represent_row(hm, y, show_ships)
                for hm, show_ships in hitmaps
            ) for y in range(hitmaps[0][0].battlefield.plane.size[1])
        )

