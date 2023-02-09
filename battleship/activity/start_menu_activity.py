from battleship.activity.activity import Activity
from battleship.activity.game_state import GameState


class StartMenuActivity(Activity):
    def __init__(self):
        self._error = None

    def run(self, console_width: int) -> (None, GameState):
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
                    "(3) Replay game\n"
                    "(0) Exit\n"
                ))
                command = int(command)
                if command == 1:
                    return None, GameState.ENTER_NAMES
                if command == 2:
                    return None, GameState.SCOREBOARD
                if command == 3:
                    return None, GameState.REPLAY
                if command == 0:
                    return None, GameState.EXIT
            except Exception:
                pass

            self._error = f"Bad input: {command}"



