import os
import sys

import pygame

pygame.init()
size = width, height = 600, 300
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image1 = pygame.transform.scale(image, (600, 300))
    return image1


image = load_image('gameover.png')

# поле 5 на 17
count = 1
running = True
x, y = -600, 0
while running:

    screen.fill((0, 0, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    if x != 0:
        x += 20
    screen.blit(image, (x, y))
    clock.tick(60)

    pygame.display.flip()
