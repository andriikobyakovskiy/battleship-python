import json
import os

from battleship.activity.activity import Activity
from battleship.activity.enter_names_acitivty import EnterNamesActivity
from battleship.activity.game_loop import GameLoop
from battleship.activity.game_stage import GameStage
from battleship.activity.place_ships_loop import PlaceShipsLoop
from battleship.activity.scoreboard_activity import ScoreboardActivity
from battleship.activity.settings_change_activity import SettingsChangeActivity
from battleship.activity.settings_selection_activity import SettingsSelectionActivity
from battleship.activity.start_menu_activity import StartMenuActivity
from battleship.activity.two_players_activity import TwoPlayersActivity
from battleship.activity.victory_activity import VictoryActivity
from battleship.model.battlefield import Battlefield
from battleship.model.battlelog import BattleLog
from battleship.model.coordinates import Plane
from battleship.model.couple import Couple
from battleship.model.settings import Settings


class ActivityPlaceholder(Activity):

    def __init__(self, state: GameStage):
        self._state = state

    def run(self, console_width: int) -> (None, GameStage):
        self.clean_console()
        input(f"State {self._state} is not implemented.\nPress Enter to return to main menu...")
        return None, GameStage.START_MENU


class MainActivity(Activity):

    def __init__(self):
        self._current_stage = GameStage.START_MENU
        self._settings = Settings()
        self._last_result = None
        self._scoreboard = []

    def run(self, console_width: int) -> (object, GameStage):
        while self._current_stage != GameStage.EXIT:
            self.clean_console()
            current_activity = self._create_current_activity()
            self._last_result, self._current_stage = current_activity.run(os.get_terminal_size()[0])
        return self._last_result, self._current_stage

    def _create_current_activity(self) -> Activity:
        if self._current_stage == GameStage.START_MENU:
            if isinstance(self._last_result, Settings):
                self._settings = self._last_result
            return StartMenuActivity()

        if self._current_stage == GameStage.ENTER_NAMES:
            return EnterNamesActivity()

        if self._current_stage == GameStage.PLACE_SHIPS:
            if not isinstance(self._last_result, list):
                raise Exception("Expected list of names as last activity result")
            battlefields = Couple({
                self._last_result[0]: Battlefield(Plane((10, 10), ("A", 1))),
                self._last_result[1]: Battlefield(Plane((10, 10), ("A", 1))),
            })
            return TwoPlayersActivity(
                players_loops=battlefields.map_values(
                    lambda bf: PlaceShipsLoop(bf, self._settings.ships_count)
                ),
                next_state=GameStage.GAME,
                activity_end_check=lambda loops: all((
                    loop.all_ships_placed()
                    for loop in loops.values()
                ))
            )

        if self._current_stage == GameStage.GAME:
            if not isinstance(self._last_result, Couple):
                raise Exception("Expected Couple of battlefields as last activity result")
            battle_log = BattleLog(self._last_result)
            return TwoPlayersActivity(
                players_loops=self._last_result.map_values(
                    lambda _: GameLoop(battle_log)
                ),
                next_state=GameStage.VICTORY,
                activity_end_check=lambda _: battle_log.winner is not None
            )

        if self._current_stage == GameStage.VICTORY:
            if not isinstance(self._last_result, Couple):
                raise Exception("Expected Couple of BattleLogs as last activity result")
            return VictoryActivity(self._last_result.current_value, self._settings)

        if self._current_stage == GameStage.SETTINGS_SELECTION:
            return SettingsSelectionActivity(self._settings)

        if self._current_stage == GameStage.SETTINGS_CHANGE:
            if not isinstance(self._last_result, str):
                raise Exception("Expected settings parameter as last activity result")
            return SettingsChangeActivity(self._settings, self._last_result)

        if self._current_stage == GameStage.SCOREBOARD:
            self._get_logs()
            return ScoreboardActivity(self._scoreboard)

        return ActivityPlaceholder(self._current_stage)

    def _get_logs(self):
        self._scoreboard.clear()
        for path in self._settings.logs_path.iterdir():
            with path.open() as f:
                self._scoreboard.append(json.load(f))

