from constants import *
from level import Level
from menu import MainManu
from state import GameState, LevelState


class Game:
    def __init__(self):
        self.state = GameState.MainManu
        self.running = True
        self.level = None
        self.main_menu = MainManu(self)

    def check_state(self, events):
        if self.state == GameState.PlayLevel:
            if self.level is None:
                self.level = Level(1, "data/map.tmx")
            else:
                level_state = self.level.get_state()
                if level_state == LevelState.Run:
                    self.level.render(events)
                elif level_state == LevelState.Win:
                    self.state = GameState.WinMenu
                    self.level = None
                elif level_state == LevelState.Lose:
                    self.state = GameState.GameOverManu
                    self.level = None
        if self.state in (
            GameState.WinMenu,
            GameState.GameOverManu,
            GameState.MainManu,
        ):
            self.main_menu.render(events)

        if self.state == GameState.Exit:
            self.running = False

    def set_state(self, state):
        self.state = state

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
