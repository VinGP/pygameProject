import pygame

from constants import *
from tools import load_image
from state import GameState


class AbstractMenu:
    """Класс абстрактного меню"""

    def __init__(self, game, background=MENU_BACKGROUND_IMAGE):
        self.game = game
        self.background = pygame.transform.scale(
            load_image(background), (WIDTH, HEIGHT)
        )
        self.buttons = pygame.sprite.Group()

        self.title = FONT.render("", True, (34, 139, 34))

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
        SCREEN.blit(self.title, (WIDTH // 2 - self.title.get_width() // 2, 15))

        self.buttons.update()
        self.buttons.draw(SCREEN)


class MainMenu(AbstractMenu):
    def __init__(self, g):
        super().__init__(g)

        self.title = FONT.render(GAME_TITLE, True, (34, 139, 34))
        SCREEN.blit(self.title, (WIDTH // 2 - self.title.get_width() // 2, 10))

        buttons = [
            {"text": "Уровни", "state": GameState.LevelMenu},
            {"text": "Выйти", "state": GameState.Exit},
        ]
        for i, button in enumerate(buttons):
            TextButton(
                WIDTH // 2, 200 + 100 * i, button["state"], button["text"], self.buttons
            )


class LevelMenu(AbstractMenu):
    def __init__(self, game):
        super().__init__(game)
        levels = self.game.db.get_all_level_user_progress()

        self.title = FONT.render("Уровни", True, (34, 139, 34))

        self.button_width, self.button_height = 100, 100
        self.margin_right = 20
        self.margin_top = 20
        self.margin_left = 20
        self.spacing = 10

        f = pygame.font.SysFont("Robot", 50)
        t = f.render("Назад", True, TextButton_TEXT_COLOR)
        w = t.get_width()
        h = t.get_height()
        TextButton(
            self.margin_left + w // 2,
            self.margin_top + h // 2,
            GameState.MainMenu,
            "Назад",
            self.buttons,
            button_text_color_mouse_motion=pygame.Color("green"),
            button_text_color=pygame.Color("forestgreen"),
            font=f,
        )

        self.margin_top += self.title.get_height()

        n = 0
        for i in range(((self.button_width + self.spacing) * len(levels) // WIDTH) + 1):
            for j in range(
                (WIDTH - self.margin_left - self.margin_right)
                // (self.button_width + self.spacing)
            ):
                LevelButton(
                    self.margin_left + (self.button_width + self.spacing) * j,
                    self.margin_top + (self.button_height + self.spacing) * i,
                    self.button_width,
                    self.button_height,
                    self.buttons,
                    GameState.PlayLevel,
                    levels[n],
                )
                n += 1
                if n > len(levels) - 1:
                    break
            else:
                continue
            break

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.check_click(*pygame.mouse.get_pos()):
                        self.game.set_state(button.state)
                        self.game.level_menu = None
                        if isinstance(button, LevelButton):
                            self.game.set_level(button.level_id)
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.mouse_motion(*pygame.mouse.get_pos())
        SCREEN.blit(self.background, (0, 0))
        SCREEN.blit(self.title, (WIDTH // 2 - self.title.get_width() // 2, 15))
        self.buttons.update()
        self.buttons.draw(SCREEN)


class EndLevel(AbstractMenu):
    star_good = load_image(r"star\star_good.png")
    star_bad = load_image(r"star\star_bad.png")

    def __init__(self, game, level_result, buttons, title):
        super().__init__(game)
        self.title = FONT.render(title, True, (34, 139, 34))

        self.stars = level_result
        self.margin_top = 15

        margin = self.margin_top + self.title.get_height()

        margin += 5 + self.star_bad.get_height() + 30

        for i, button in enumerate(buttons):
            TextButton(
                WIDTH // 2,
                margin + 100 * i + self.margin_top,
                button["state"],
                button["text"],
                self.buttons,
            )

        self.margin = margin

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.check_click(*pygame.mouse.get_pos()):
                        self.game.set_state(button.state)
                        self.game.win_menu = None
                        self.game.lose_menu = None

            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.mouse_motion(*pygame.mouse.get_pos())
        SCREEN.blit(self.background, (0, 0))

        x = WIDTH // 2 - ((self.star_bad.get_width() + 5) * 3) // 2
        for i in range(3):
            if self.stars - i > 0:
                SCREEN.blit(
                    self.star_good,
                    (
                        x + (self.star_good.get_width() + 5) * i,
                        self.margin - self.star_good.get_height() - 30,
                    ),
                )
            else:
                SCREEN.blit(
                    self.star_bad,
                    (
                        x + (self.star_bad.get_width() + 5) * i,
                        self.margin - self.star_bad.get_height() - 30,
                    ),
                )

        SCREEN.blit(
            self.title, (WIDTH // 2 - self.title.get_width() // 2, self.margin_top)
        )
        self.buttons.update()
        self.buttons.draw(SCREEN)


class WinMenu(EndLevel):
    def __init__(self, game, level_id, level_result):
        buttons = [
            {"text": "Пройти ещё раз", "state": GameState.ReplayLevel},
        ]
        self.game = game

        try:
            next_level = self.game.db.get_level(level_id + 1)
            buttons.append({"text": "Следующий уровень", "state": GameState.NextLevel})
        except Exception:
            pass

        buttons.extend(
            [
                {"text": "Все уровни", "state": GameState.LevelMenu},
                # {"text": "Главное меню", "state": GameState.MainMenu},
                {"text": "Выйти", "state": GameState.Exit},
            ]
        )
        super().__init__(
            game, level_result, buttons, title=f"Уровень {level_id} завершён!"
        )


class LoseMenu(EndLevel):
    def __init__(self, game):
        buttons = [
            {"text": "Попробовать ещё раз", "state": GameState.ReplayLevel},
            {"text": "Все уровни", "state": GameState.LevelMenu},
            # {"text": "Главное меню", "state": GameState.MainMenu},
            {"text": "Выйти", "state": GameState.Exit},
        ]

        super().__init__(game, level_result=0, buttons=buttons, title="Вы проиграли!")


class AbstractButton(pygame.sprite.Sprite):
    """Класс абстрактной кнопки на которую можно нажать"""

    def __init__(self, x, y, width, height, group):
        super().__init__(group)
        self.image = pygame.Surface(
            (width, height), pygame.SRCALPHA, 32
        )  # Прозрачный surface
        self.rect = pygame.rect.Rect(x, y, width, height)

    def check_click(self, x, y):
        """Метод который, проверяет нажатие на кнопку"""
        return self.rect.collidepoint(x, y)


class TextButton(AbstractButton):
    def __init__(
        self,
        x,
        y,
        state,
        text,
        group,
        button_text_color=TextButton_TEXT_COLOR,
        button_text_color_mouse_motion=TextButton_TEXT_COLOR_MOUSE_MOTION,
        font=FONT,
    ):
        """
        :param x: координата центра кнопки
        :param y: координата центра кнопки
        :param state: состояние в которое переводит кнопка
        :param text: текст на кнопке
        :param group: группа кнопок
        """

        self.text = text
        self.font = font
        self.default_color_text = button_text_color
        self.mouse_motion_color_text = button_text_color_mouse_motion
        self.color_text = self.default_color_text
        self.button_text = self.font.render(
            self.text,
            True,
            self.color_text,
        )

        self.state = state  # Состояние игры на которое переносит эта кнопка
        super().__init__(
            x - self.button_text.get_width() // 2,
            y - self.button_text.get_height() // 2,
            *self.button_text.get_size(),
            group=group,
        )
        self.image.blit(self.button_text, (0, 0))

    def update_color(self):
        self.button_text = self.font.render(
            self.text,
            True,
            self.color_text,
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


class LevelButton(AbstractButton):
    star_good = load_image(r"star\star_good.png")
    star_bad = load_image(r"star\star_bad.png")

    def __init__(
        self,
        x,
        y,
        width,
        height,
        group,
        state,
        level_data,
        button_color=LevelButton_BACGROUND_COLOR,
        mouse_motion_button_color=LevelButton_BACGROUND_COLOR_MOUSE_MOTION,
    ):
        super().__init__(x, y, width, height, group)
        self.state = state  # Состояние игры на которое переносит эта кнопка
        self.level_id = level_data.id
        self.text = str(level_data.id)
        self.stars = level_data.stars

        self.button_text = FONT.render(self.text, True, pygame.Color("black"))

        self.star_size = min(
            self.image.get_width() // 3,
            self.image.get_height() - self.button_text.get_height(),
        )

        self.star_bad = pygame.transform.scale(
            self.star_bad,
            (
                self.star_size,
                self.star_size,
            ),
        )
        self.star_good = pygame.transform.scale(
            self.star_good,
            (
                self.star_size,
                self.star_size,
            ),
        )

        self.default_button_color = button_color
        self.mouse_motion_button_color = mouse_motion_button_color
        self.button_color = self.default_button_color
        self.render()

    def render(self):
        self.image.fill(self.button_color)

        self.image.blit(
            self.button_text,
            (self.image.get_width() // 2 - self.button_text.get_width() // 2, 4),
        )
        for i in range(3):
            if self.stars - i > 0:
                self.image.blit(
                    self.star_good,
                    (
                        self.image.get_width() // 3 * i,
                        self.image.get_height()
                        - self.star_good.get_height()
                        - (
                            self.image.get_height()
                            - self.button_text.get_height()
                            - self.star_good.get_height()
                        )
                        // 2,
                    ),
                )
            else:
                self.image.blit(
                    self.star_bad,
                    (
                        self.image.get_width() // 3 * i,
                        self.image.get_height()
                        - self.star_bad.get_height()
                        - (
                            self.image.get_height()
                            - self.button_text.get_height()
                            - self.star_bad.get_height()
                        )
                        // 2,
                    ),
                )

    def mouse_motion(self, x, y):
        if self.rect.collidepoint(x, y):
            if self.button_color == self.default_button_color:
                self.button_color = self.mouse_motion_button_color
                self.render()
        elif self.button_color != self.default_button_color:
            self.button_color = self.default_button_color
            self.render()
