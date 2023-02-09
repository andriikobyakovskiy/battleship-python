from typing import List

from battleship.activity.activity import Activity
from battleship.activity.game_state import GameState


class EnterNamesActivity(Activity):

    def run(self, _) -> (List[str], GameState):
        first_player = None
        while not first_player:
            first_player = input("Enter first player's name:\n>>> ")
        second_player = None
        while not second_player or second_player == first_player:
            if second_player == first_player:
                print("PLayers' names cannot be same")
            second_player = input("Enter second player's name:\n>>> ")

        return [first_player, second_player], GameState.PLACE_SHIPS
