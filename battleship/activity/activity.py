import os
from abc import ABC, abstractmethod

from battleship.activity.game_stage import GameStage


class Activity(ABC):
    """
    Class that manages user interaction flow
    """

    @staticmethod
    def clean_console():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @abstractmethod
    def run(self, console_width: int) -> (object, GameStage):
        ...
