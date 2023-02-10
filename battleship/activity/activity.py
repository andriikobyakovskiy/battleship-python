import os
from abc import ABC, abstractmethod

from battleship.activity.game_state import GameStage


class Activity(ABC):

    @staticmethod
    def clean_console():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @abstractmethod
    def run(self, console_width: int) -> (object, GameStage):
        ...
