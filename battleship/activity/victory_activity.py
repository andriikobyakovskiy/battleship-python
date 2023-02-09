from battleship.activity.activity import Activity
from battleship.activity.game_state import GameState
from battleship.model.battlelog import BattleLog
from battleship.model.settings import Settings


class VictoryActivity(Activity):

    def __init__(self, battle_log: BattleLog, settings: Settings):
        self._log = battle_log
        self._settings = settings

    def run(self, console_width: int) -> (object, GameState):
        while True:
            self.clean_console()
            print(f"Player {self._log.winner} is winner!")
            response = input(f"\nDo you want to save log at {self._settings.logs_path}? (y/n)\n>>> ")
            if response == 'y':
                break

            if response == 'n':
                break

        return self._log, GameState.START_MENU
