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
            # self._players_switch_placeholder(self._functions.current_key)
            # self.clean_console()
            input(f"Awaiting for player {self._loops.current_key}.\nPress Enter to continue...")
            result = None
            while not self._loops.current_value.turn_end_check(result):
                # self.clean_console()
                if self._error:
                    print(self._error)
                result = self._loops.current_value.run_iteration(console_width)
                self._error = self._loops.current_value.get_error_from_result(result)
            self._loops.switch_current()
        return self._loops.map_values(lambda loop: loop.get_activity_result()), self._next_state

# class TwoPlayersActivity(Activity, Generic[E]):
#
#     def __init__(
#         self,
#         next_state: GameState,
#         players_functions: Couple[Callable],
#         turn_end_check: Callable[[object], bool],
#         activity_end_check: Callable[[object], bool],
#         get_error_from_result: Callable[[object], Optional[str]],
#         # players_switch_placeholder: Callable[[str], None],
#     ):
#         self._next_state = next_state
#         self._functions = players_functions
#         self._turn_end_check = turn_end_check
#         self._activity_end_check = activity_end_check
#         # self._players_switch_placeholder = players_switch_placeholder
#         self._get_error_from_result = get_error_from_result
#         self._error = None
#
#     def run(self, console_width: int):
#         result = None
#         while not self._activity_end_check(result):
#             # self._players_switch_placeholder(self._functions.current_key)
#             input(f"Awaiting for player {self._functions.current_key}.\nPress Enter to continue...")
#             while self._turn_end_check(result):
#                 self.clean_console()
#                 if self._error:
#                     print(self._error)
#                 result = self._functions.current_value(console_width)
#                 self._error = self._get_error_from_result(result)
#             self._functions.switch_current()
#         return self._next_state
