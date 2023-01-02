from enum import Enum
from constants import *
from level import Level


class State(Enum):
    MainManu = 0
    LevelManu = 1
    PlayLevel = 2
    StopLevel = 3


class Game:
    def __init__(self):
        self.state = State.PlayLevel
        self.running = True
        self.level = Level(1, "data/map.tmx")

    def check_state(self, events):
        if self.state == State.PlayLevel:
            self.level.update(events)

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
