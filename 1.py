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
    show_menu_f = True
    start_btn = Button(300, 70)
    while show_menu_f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu_f = False

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
    game_cycle_show = True
    story_mode_btn = Button(460, 100)
    pvp_btn = Button(460, 100)
    while game_cycle_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_cycle_show = False

        screen.blit(menu_background, (0, 0))
        story_mode_btn.draw(80, 80, 'Story mode', 'btn.png', story_mode)
        pvp_btn.draw(730, 80, 'PVP mode', 'btn.png', pvp_mode)
        pygame.display.update()


def story_mode():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background_5.jpg')
    story_mode_show = True
    new_game = Button(540, 150)
    store = Button(460, 100)
    heroes = Button(460, 100)
    while story_mode_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    story_mode_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(360, 80, 'NEW GAME', 'btn.png', story_mode_new_game)
        store.draw(400, 260, 'STORE', 'btn.png', store_mode)
        heroes.draw(400, 400, 'HEROES', 'btn.png')

        pygame.display.update()


def story_mode_new_game():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/for_nickname.jpg')
    story_mode_new_game_show = True
    new_game = Button(380, 70)
    while story_mode_new_game_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    story_mode_new_game_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(880, 600, 'ok', 'btn.png', story_mode_new_game_select_heroes)
        pygame.display.update()


def story_mode_new_game_select_heroes():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/select_heroes.jpg')
    story_mode_new_game_select_heroes_show = True
    new_game = Button(380, 70)
    while story_mode_new_game_select_heroes_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    story_mode_new_game_select_heroes_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(450, 620, 'select', 'btn.png', levels_show_menu)
        pygame.display.update()


def levels_show_menu():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/start_level.jpg')
    levels_show = True
    new_game = Button(500, 100)
    while levels_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    levels_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(700, 560, 'start', 'btn.png', game)
        pygame.display.update()


def pvp_mode():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    pvp_mode_show = True
    new_game = Button(250, 70)
    while pvp_mode_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pvp_mode_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'select', 'btn.png', pvp_mode_2)
        new_game.draw(515, 500, 'select', 'btn.png', pvp_mode_2)
        new_game.draw(885, 500, 'select', 'btn.png', pvp_mode_2)
        pygame.display.update()


def pvp_mode_2():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    pvp_mode_2_show = True
    new_game = Button(250, 70)
    while pvp_mode_2_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pvp_mode_2_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'start', 'btn.png', play_pvp_mode)
        new_game.draw(515, 500, 'start', 'btn.png', play_pvp_mode)
        new_game.draw(885, 500, 'start', 'btn.png', play_pvp_mode)
        pygame.display.update()


def game():
    pass


def play_pvp_mode():
    pass


def store_mode():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    story_mode_new_game_show = True
    new_game = Button(250, 70)
    while story_mode_new_game_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    story_mode_new_game_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'select', 'btn.png', buy_mage)
        new_game.draw(515, 500, 'select', 'btn.png', buy_warrior)
        new_game.draw(885, 500, 'select', 'btn.png', buy_archer)
        pygame.display.update()


def buy_mage():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    buy_mage_show = True
    new_game = Button(250, 70)
    while buy_mage_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    buy_mage_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(515, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(885, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        pygame.display.update()


def buy_warrior():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    buy_warrior_show = True
    new_game = Button(250, 70)
    while buy_warrior_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    buy_warrior_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(515, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(885, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        pygame.display.update()


def buy_archer():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/buy_skin.jpg')
    buy_archer_show = True
    new_game = Button(250, 70)
    while buy_archer_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    buy_archer_show = False

        screen.blit(menu_background, (0, 0))
        new_game.draw(145, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(515, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        new_game.draw(885, 500, 'buy', 'btn.png', story_mode_new_game_select_heroes)
        pygame.display.update()


if __name__ == '__main__':
    start_menu()
