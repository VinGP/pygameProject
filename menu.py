from constants import *
from tools import load_image


class AbstractMenu:
    """Класс абстрактного меню"""

    def __init__(self, game, background=MENU_BACKGROUND_IMAGE):
        self.game = game
        self.background = pygame.transform.scale(
            load_image(background), (WIDTH, HEIGHT)
        )
        self.buttons = pygame.sprite.Group()

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.check_click(*pygame.mouse.get_pos()):
                        self.game.set_state(button.state)
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.mouse_motion(*pygame.mouse.get_pos())
        SCREEN.blit(self.background, (0, 0))

        self.buttons.update()
        self.buttons.draw(SCREEN)


class MainManu(AbstractMenu):
    def __init__(self, g):
        super().__init__(g)
        from state import GameState

        buttons = [
            # {"text": "Уровни", "state": GameState.PlayLevel},
            {"text": "Начать игру", "state": GameState.PlayLevel},
            {"text": "Выйти", "state": GameState.Exit},
        ]
        for i, button in enumerate(buttons):
            TextButton(
                WIDTH // 2, 200 + 100 * i, button["state"], button["text"], self.buttons
            )


class AbstractButton(pygame.sprite.Sprite):
    """Класс абстрактной кнопки на которую можно нажать"""

    def __init__(self, x, y, width, height, group):
        super().__init__(group)
        self.image = pygame.Surface(
            (width, height), pygame.SRCALPHA, 32
        )  # Прозрачный surface
        self.rect = pygame.rect.Rect(x, y, width, height)

    def check_click(self, x, y):
        """Метод который проверяет нажали ли на кнопку"""
        return self.rect.collidepoint(x, y)


class TextButton(AbstractButton):
    def __init__(self, x, y, state, text, group):
        """
        :param x: координата центра кнопки
        :param y: координата центра кнопки
        :param state: состояние в которое переводит кнопка
        :param text: текст на кнопке
        :param group: группа кнопок
        """
        self.text = text
        self.font = FONT
        self.button_text = self.font.render(
            self.text,
            True,
            pygame.color.Color("black"),
        )

        self.state = state  # Состояние игры на которое переносит эта кнопка
        super().__init__(
            x - self.button_text.get_width() // 2,
            y - self.button_text.get_height() // 2,
            *self.button_text.get_size(),
            group=group
        )
        self.image.blit(self.button_text, (0, 0))

        self.default_color_text = "black"
        self.mouse_motion_color_text = "red"
        self.color_text = self.default_color_text

    def update_color(self):
        self.button_text = self.font.render(
            self.text,
            True,
            pygame.color.Color(self.color_text),
        )
        self.image = pygame.Surface(self.button_text.get_size(), pygame.SRCALPHA, 32)
        self.image.blit(self.button_text, (0, 0))

    def mouse_motion(self, x, y):
        if self.rect.collidepoint(x, y):
            if self.color_text == self.default_color_text:
                self.color_text = self.mouse_motion_color_text
                self.update_color()
        elif self.color_text != self.default_color_text:
            self.color_text = self.default_color_text
            self.update_color()
