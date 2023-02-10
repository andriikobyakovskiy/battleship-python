import dataclasses
import json
from uuid import uuid4

from battleship.activity.activity import Activity
from battleship.activity.game_state import GameStage
from battleship.model.battlefield import Ship
from battleship.model.battlelog import BattleLog
from battleship.model.settings import Settings


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Ship.Orientation):
            return o.value
        return super().default(o)


class VictoryActivity(Activity):

    def __init__(self, battle_log: BattleLog, settings: Settings):
        self._log = battle_log
        self._settings = settings

    def run(self, console_width: int) -> (object, GameStage):
        while True:
            self.clean_console()
            print(f"Player {self._log.winner} is winner!")
            response = input(f"\nDo you want to save log at {self._settings.logs_path}? (y/n)\n>>> ")
            if response == 'y':
                if not self._settings.logs_path.exists():
                    self._settings.logs_path.mkdir()
                with self._settings.logs_path.joinpath(f"{uuid4()}.json").open("w") as f:
                    json.dump(self._log.to_dict(), f, cls=EnhancedJSONEncoder)
                break

            if response == 'n':
                break

        return self._log, GameStage.START_MENU
