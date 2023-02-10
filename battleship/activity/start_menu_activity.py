from battleship.activity.activity import Activity
from battleship.activity.game_state import GameStage


class StartMenuActivity(Activity):
    def __init__(self):
        self._error = None

    def run(self, console_width: int) -> (None, GameStage):
        result = None
        command = None
        while not result:
            try:
                self.clean_console()
                if self._error:
                    print(self._error)
                command = input((
                    "Enter action number:\n"
                    "(1) Start new game\n"
                    "(2) Show top scores\n"
                    "(3) Change settings\n"
                    "(0) Exit\n>>> "
                ))
                command = int(command)
                if command == 1:
                    return None, GameStage.ENTER_NAMES
                if command == 2:
                    return None, GameStage.SCOREBOARD
                if command == 3:
                    return None, GameStage.SETTINGS_SELECTION
                if command == 0:
                    return None, GameStage.EXIT
            except Exception:
                pass

            self._error = f"Bad input: {command}"



