from enum import Enum


class GameState(Enum):
    MainManu = 0
    LevelManu = 1
    PlayLevel = 2
    StopLevel = 3
    WinMenu = 4
    GameOverManu = 5
    Exit = 6


class LevelState(Enum):
    Run = 0
    Win = 1
    Lose = 2
