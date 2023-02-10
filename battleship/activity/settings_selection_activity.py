from dataclasses import fields
from typing import Tuple

from battleship.activity.activity import Activity
from battleship.activity.game_state import GameState
from battleship.model.coordinates import Coordinates
from battleship.model.settings import Settings


class SettingsSelectionActivity(Activity):
    def __init__(self, settings: Settings):
        self._settings = settings
        self._error = None

    def run(self, console_width: int) -> (object, GameState):
        field = None
        while True:
            try:
                self.clean_console()
                if self._error:
                    print(self._error)
                print(f"Current settings: {self._settings}")
                field_values = [
                    field.name
                    for field in fields(self._settings)
                    # do not allow to modify coordinates conversion
                    if field.type not in (Tuple[int, int], Coordinates)
                ]
                field = input(
                    "Enter parameter to change:\n" +
                    "\n".join(field_values) +
                    "\nexit\n>>> "
                )
                if field == "exit":
                    return None, GameState.START_MENU
                if field in field_values:
                    return field, GameState.SETTINGS_CHANGE
            except Exception:
                pass

            self._error = f"No such parameter: {field}"
