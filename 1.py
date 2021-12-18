import logging
import os
import sys
from time import sleep

import pygame

pygame.init()
pygame.display.set_caption('pygame-project')
# screen = pygame.display.set_mode((1280, 720),
# pygame.FULLSCREEN) с fullscreen не удобно при написании, потом поставим

screen = pygame.display.set_mode((1280, 720))

MENU_ACTIVE_BTN_COLOR = pygame.Color('#40009A')
MENU_INACTIVE_BTN_COLOR = pygame.Color('#8130F4')
MENU_BTN_SOUND = pygame.mixer.Sound('sounds/menu_btn.wav')


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
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
    return image


class Button:
    """
    Класс кнопок для создания непосредственно самих конпок
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = MENU_INACTIVE_BTN_COLOR
        self.active_color = MENU_ACTIVE_BTN_COLOR

    def draw(self, x, y, message, button_image, action=None, font_size=50):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)),
                        (x, y - 5))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
            x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2) - 5))
            if clicked[0]:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
            x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))


def show_menu(screen):
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background.jpg')
    show = True
    start_btn = Button(300, 70)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(430, 200, 'Start game', 'btn.png', game_cycle)
        pygame.display.update()


def start_menu():
    running = True
    clock = pygame.time.Clock()
    show_menu(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tick = clock.tick()
        pygame.display.flip()
    pygame.quit()


def game_cycle():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background_2.jpg')
    show = True
    story_mode_btn = Button(460, 100)
    pvp_btn = Button(460, 100)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        story_mode_btn.draw(80, 80, 'Story mode', 'btn.png', story_mode)
        pvp_btn.draw(730, 80, 'PVP mode', 'btn.png', pvp_mode)
        pygame.display.update()


def story_mode():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background_3.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        pygame.display.update()


def pvp_mode():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background_4.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    start_menu()
