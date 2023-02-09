from enum import Enum


class GameState(Enum):
    START_MENU = 'SM'
    ENTER_NAMES = 'E'
    PLACE_SHIPS = 'P'
    GAME = 'G'
    VICTORY = 'V'
    SCOREBOARD = 'SB'
    SETTINGS = 'S'
    REPLAY = 'R'
    EXIT = 'X'
