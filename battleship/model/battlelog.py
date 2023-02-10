from typing import Optional, List, Tuple
from dataclasses import dataclass

from battleship.model.battlefield import Ship, Battlefield
from battleship.model.coordinates import Coordinates
from battleship.model.couple import Couple
from battleship.model.exceptions import CoordinatesValueException


@dataclass(frozen=True)
class BattleMove:
    player: str
    target: Coordinates


@dataclass(frozen=False)
class HitmapCell:
    was_hit: bool = False
    contents: Optional[Ship] = None


@dataclass(frozen=True)
class Hitmap:
    map: List[List[HitmapCell]]
    battlefield: Battlefield


class BattleLog:
    _hitmaps: Couple[Hitmap]
    _battlefields: Couple[Battlefield]
    _battle_log: List[BattleMove]

    def __init__(self, battlefields: Couple[Battlefield]):
        self._battlefields = battlefields
        self._hitmaps = Couple({
            player: Hitmap(
                [
                    [HitmapCell() for y in range(bf.plane.size[0])]
                    for x in range(bf.plane.size[0])
                ],
                bf
            )
            for player, bf in self._battlefields.items()
        })
        for player, bf in self._battlefields.items():
            self._hitmaps.set_current(player)
            for ship in bf.ships:
                for c in ship.coordinates:
                    x, y = bf.plane.to_local_coordinates(c)
                    self._hitmaps.current_value.map[x][y].contents = ship
        self._hitmaps.switch_current()
        self._battle_log = []

    def get_marked_hitmaps(self) -> List[Tuple[Hitmap, bool]]:
        return [
            (self._hitmaps.another_value, False),
            (self._hitmaps.current_value, True),
        ]

    @property
    def current_player(self) -> str:
        return self._hitmaps.current_key

    @property
    def winner(self) -> Optional[str]:
        for player, hitmap in self._hitmaps.items():
            if all(cell.was_hit
                   for column in hitmap.map
                   for cell in column
                   if cell.contents is not None):
                return self._hitmaps.another_key if self.current_player == player else self.current_player

    def make_move(self, target: Coordinates) -> bool:
        bf_plane = self._battlefields.current_value.plane
        if target not in bf_plane:
            raise CoordinatesValueException(f"Coordinates {target} are out of battlefield")

        x, y = bf_plane.to_local_coordinates(target)
        self._hitmaps.another_value.map[x][y].was_hit = True
        result = self._hitmaps.another_value.map[x][y].contents
        self._battle_log.append(
            BattleMove(
                player=self._hitmaps.current_key,
                target=target
            )
        )
        if result is None:
            self._hitmaps.switch_current()
            self._battlefields.switch_current()
            return False
        return True
