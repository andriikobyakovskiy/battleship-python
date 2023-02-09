from typing import Callable

from battleship.activity.activity import Activity
from battleship.activity.game_state import GameState
from battleship.activity.single_player_loop import SinglePlayerLoop
from battleship.model.couple import Couple


class TwoPlayersActivity(Activity):

    def __init__(
        self,
        next_state: GameState,
        loops: Couple[SinglePlayerLoop],
        activity_end_check: Callable[[Couple[SinglePlayerLoop]], bool],
    ):
        self._next_state = next_state
        self._loops = loops
        self._activity_end_check = activity_end_check
        self._error = None

    def run(self, console_width: int):
        while not self._activity_end_check(self._loops):
            self.clean_console()
            input(f"Awaiting for player {self._loops.current_key}.\nPress Enter to continue...")
            result = None
            while not self._loops.current_value.turn_end_check(result):
                self.clean_console()
                if self._error:
                    print(self._error)
                result = self._loops.current_value.run_iteration(console_width)
                self._error = self._loops.current_value.get_error_from_result(result)
            self._loops.switch_current()
        return self._loops.map_values(lambda loop: loop.get_activity_result()), self._next_state
