from battleship.activity.activity import Activity
from battleship.activity.game_state import GameStage
from battleship.model.settings import Settings


class SettingsChangeActivity(Activity):

    FORMAT_HINTS = {
        "ships_count": "5:2,3:0",
        "logs_path": "/home/user/games/battleship",
    }

    def __init__(self, settings: Settings, parameter: str):
        self._settings = settings
        self._parameter = parameter
        self._error = None

    def run(self, console_width: int) -> (object, GameStage):
        result = None
        while not result:
            try:
                self.clean_console()
                if self._error:
                    print(self._error)
                print(f"Current value: {getattr(self._settings, self._parameter)}")
                new_value = input(f"Enter new value (for example {self.FORMAT_HINTS[self._parameter]}):\n>>> ")
                if self._parameter == "ships_count":
                    for pair in new_value.split(","):
                        [index, value] = pair.split(":")
                        i = int(index)
                        v = int(value)
                        if 0 < i < 6 and 0 <= v < 4:
                            self._settings.ships_count[i] = v
                        else:
                            self._error = f"Ships length can be 1-5 and ships count can be 0-4"
                if self._parameter == "logs_path":
                    # a lot to check here, just trust user
                    self._settings.logs_path = new_value

                result = True

            except Exception as e:
                self._error = e.args[0]

        return self._settings, GameStage.SETTINGS_SELECTION
