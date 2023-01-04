from constants import *
from level import Level
from menu import MainMenu, LevelMenu, WinMenu
from state import GameState, LevelState
from data_base import DataBase


class Game:
    def __init__(self):
        self.state = GameState.MainMenu
        self.running = True
        self.current_level_id = None
        self.level = None
        self.main_menu = MainMenu(self)
        self.level_menu = None
        self.db = DataBase()
        self.win_menu = None

    def check_state(self, events):
        if self.state == GameState.PlayLevel:
            if self.level is None:
                self.set_level(self.current_level_id)
            else:
                level_state = self.level.get_state()
                if level_state == LevelState.Run:
                    self.level.render(events)
                elif level_state == LevelState.Win:
                    self.db.update_user_level_progress(
                        self.current_level_id, self.level.get_result()
                    )
                    self.state = GameState.WinMenu
                elif level_state == LevelState.Lose:
                    self.state = GameState.GameOverMenu

        if self.state == GameState.WinMenu:
            if not self.win_menu:
                self.win_menu = WinMenu(
                    self, self.current_level_id, self.level.get_result()
                )
            else:
                self.win_menu.render(events)

        if self.state in (
            GameState.GameOverMenu,
            GameState.MainMenu,
        ):
            self.main_menu.render(events)

        if self.state == GameState.LevelMenu:
            if self.level_menu:
                self.level_menu.render(events)
            else:
                self.level_menu = LevelMenu(self)

        if self.state == GameState.NextLevel:
            self.set_level(self.current_level_id + 1)
            self.state = GameState.PlayLevel

        if self.state == GameState.Exit:
            self.running = False

    def set_state(self, state):
        self.state = state

    def set_level(self, level_id):
        self.current_level_id = level_id
        del self.level
        level = self.db.get_level(self.current_level_id)
        self.level = Level(
            level_id=level.id,
            level_map_file_path=level.map_path,
            count_crystals=level.count_crystal,
        )

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.check_state(events)
            clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()
