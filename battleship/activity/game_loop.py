from dataclasses import dataclass
from typing import Optional
import re

from battleship.activity.single_player_loop import SinglePlayerLoop
from battleship.model.battlelog import BattleLog
from battleship.model.exceptions import CoordinatesValueException
from battleship.representation.hitmap_representation import HitmapRepresentation


class MoveResult:
    pass


@dataclass
class Error(MoveResult):
    message: str


class Hit(MoveResult):
    pass


class Miss(MoveResult):
    pass


class GameLoop(SinglePlayerLoop[MoveResult]):

    def __init__(self, battle_log: BattleLog):
        self.battle_log = battle_log
        self._target_regexp = re.compile(r"(?P<x>[A-Ja-j])(?P<y>[1-9]|10)")

    def run_iteration(self, console_width: int) -> MoveResult:

        print(HitmapRepresentation(self.battle_log.get_marked_hitmaps()).get_representation(console_width))
        final_input = input((
            "Enter any target coordinate (for example 'A1')\n"
            ">>> "
        ))
        match_target = self._target_regexp.fullmatch(final_input)
        if match_target:
            return self._check_target(**match_target.groupdict())

        return Error("Cannot parse coordinates")

    def _check_target(self, x, y):
        try:
            result = self.battle_log.make_move((x.upper(), int(y)))
        except CoordinatesValueException as e:
            return Error(e.args[0])
        if result:
            return Hit()
        else:
            return Miss()

    def turn_end_check(self, event_object: MoveResult) -> bool:
        return event_object is not None and isinstance(event_object, Miss) or self.battle_log.winner is not None

    def get_error_from_result(self, event_object: MoveResult) -> Optional[str]:
        return event_object.message if event_object is not None and isinstance(event_object, Error) else None

    def get_activity_result(self) -> object:
        return self.battle_log
