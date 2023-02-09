import os

from battleship.activity.activity import Activity
from battleship.activity.enter_names_acitivty import EnterNamesActivity
from battleship.activity.game_state import GameState
from battleship.activity.place_ships_loop import PlaceShipsLoop
from battleship.activity.start_menu_activity import StartMenuActivity
from battleship.activity.two_players_activity import TwoPlayersActivity
from battleship.model.battlefield import Battlefield
from battleship.model.coordinates import Plane
from battleship.model.couple import Couple
from battleship.model.settings import Settings


class ActivityPlaceholder(Activity):

    def __init__(self, state: GameState):
        self._state = state

    def run(self, console_width: int) -> (None, GameState):
        self.clean_console()
        input(f"State {self._state} is not implemented.\nPress Enter to return to main menu...")
        return None, GameState.START_MENU


class MainActivity(Activity):

    def __init__(self):
        self._current_state = GameState.START_MENU
        self._settings = Settings()
        self._last_result = None

    def run(self, console_width: int):
        while self._current_state != GameState.EXIT:
            self.clean_console()
            current_activity = self._create_current_activity()
            self._last_result, self._current_state = current_activity.run(os.get_terminal_size()[0])
        return None, GameState.EXIT

    def _create_current_activity(self) -> Activity:
        if self._current_state == GameState.START_MENU:
            return StartMenuActivity()
        if self._current_state == GameState.ENTER_NAMES:
            return EnterNamesActivity()
        if self._current_state == GameState.PLACE_SHIPS:
            if not isinstance(self._last_result, list):
                raise Exception("Expected list of names as last activity result")
            battlefields = Couple({
                self._last_result[0]: Battlefield(Plane((10, 10), ("A", 1))),
                self._last_result[1]: Battlefield(Plane((10, 10), ("A", 1))),
            })
            return TwoPlayersActivity(
                loops=battlefields.map_values(
                    lambda bf: PlaceShipsLoop(bf, self._settings.ships_count)
                ),
                next_state=GameState.START_MENU,
                activity_end_check=lambda loops: all((
                    loop.all_ships_placed()
                    for loop in loops.values()
                ))
                # turn_end_check=lambda result: not isinstance(result, PlacingError),
                # activity_end_check=lambda result: isinstance(result, PlacingReady),
                # get_error_from_result=lambda result: result.message if isinstance(result, PlacingError) else None,
                # players_switch_placeholder=lambda next_player: input(
                #     f"Awaiting for player {next_player}. Press Enter to continue..."
                # ),
            )

        return ActivityPlaceholder(self._current_state)
