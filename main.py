import pygame
import os


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
pygame.display.set_caption("Название")
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

fps = 60

clock = pygame.time.Clock()
if __name__ == "__main__":

    screen.fill((0, 0, 0))
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
