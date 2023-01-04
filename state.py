from enum import Enum


class GameState(Enum):
    MainMenu = 0
    LevelMenu = 1
    PlayLevel = 2
    StopLevel = 3
    WinMenu = 4
    LoseMenu = 5
    NextLevel = 6
    ReplayLevel = 7
    Exit = 8


class LevelState(Enum):
    Run = 0
    Win = 1
    Lose = 2
