from typing import Callable

from battleship.activity.activity import Activity
from battleship.activity.game_stage import GameStage
from battleship.activity.single_player_loop import SinglePlayerLoop
from battleship.model.couple import Couple


class TwoPlayersActivity(Activity):

    def __init__(
        self,
        next_state: GameStage,
        players_loops: Couple[SinglePlayerLoop],
        activity_end_check: Callable[[Couple[SinglePlayerLoop]], bool],
    ):
        self._next_state = next_state
        self._players_loops = players_loops
        self._activity_end_check = activity_end_check
        self._error = None

    def run(self, console_width: int):
        while not self._activity_end_check(self._players_loops):
            self.clean_console()
            input(f"Awaiting for player {self._players_loops.current_key}.\nPress Enter to continue...")
            result = None
            while not self._players_loops.current_value.turn_end_check(result):
                self.clean_console()
                if self._error:
                    print(self._error)
                result = self._players_loops.current_value.run_iteration(console_width)
                self._error = self._players_loops.current_value.get_error_from_result(result)
            self._players_loops.switch_current()
        return self._players_loops.map_values(lambda loop: loop.get_activity_result()), self._next_state
