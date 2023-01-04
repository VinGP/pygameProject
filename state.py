from enum import Enum


class GameState(Enum):
    MainMenu = 0
    LevelMenu = 1
    PlayLevel = 2
    StopLevel = 3
    WinMenu = 4
    GameOverMenu = 5
    NextLevel = 6
    Exit = 7


class LevelState(Enum):
    Run = 0
    Win = 1
    Lose = 2
