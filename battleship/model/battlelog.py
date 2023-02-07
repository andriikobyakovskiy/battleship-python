from typing import Optional, Dict, List
from dataclasses import dataclass

from battleship.model.battlefield import Ship, Battlefield
from battleship.model.coordinates import Coordinates


@dataclass(frozen=True)
class BattleMove:
    player: str
    target: Coordinates


@dataclass(frozen=False)
class BattlefieldCell:
    was_hit: bool = False
    contents: Optional[Ship] = None


class BattleLog:
    _hitmaps: Dict[str, List[List[BattlefieldCell]]]
    _battlefields: Dict[str, Battlefield]
    _current_player: str
    _battle_log: List[BattleMove]

    def __init__(self, battlefields: Dict[str, Battlefield]):
        self._battlefields = battlefields.copy()
        self._hitmaps = {
            player: [
                [ BattlefieldCell() for y in range(bf.plane.size[0]) ]
                for x in range(bf.plane.size[0])
            ]
            for player, bf in self._battlefields.items()
        }
        for player, bf in self._battlefields.items():
            for ship in bf.ships:
                for c in ship.coordinates:
                    self._hitmaps[player][c[0]][c[1]].contents = ship
        self._current_player = next(iter(self._battlefields.keys()))
        self._battle_log = []

    @property
    def hitmaps(self) -> Dict[str, List[List[BattlefieldCell]]]:
        return {
            player: [
                [ BattlefieldCell(cell.was_hit, cell.contents) for cell in column ]
                for column in hitmap
            ]
            for player, hitmap in self._hitmaps.items()
        }

    @property
    def current_player(self) -> str:
        return self._current_player

    @property
    def winner(self) -> Optional[str]:
        for player, hitmap in self._hitmaps.items():
            if all(cell.was_hit
                   for column in hitmap
                   for cell in column
                   if cell.contents is not None):
                return player

    def make_move(self, target: Coordinates) -> Optional[str]:
        bf_plane = self._battlefields[self._current_player].plane
        if target not in bf_plane:
            return

        x, y = bf_plane.to_local_coordinates(target)
        self._hitmaps[self._current_player][x][y].was_hit = True
        self._battle_log.append(
            BattleMove(
                player=self._current_player,
                target=target
            )
        )
        self._current_player = [
            player
            for player in self._battlefields
            if player != self._current_player
        ][0]
