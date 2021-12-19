import logging
import os
import sys
from time import sleep

import pygame

pygame.init()
pygame.display.set_caption('pygame-project')
# screen = pygame.display.set_mode((1280, 720),
# pygame.FULLSCREEN) с fullscreen не удобно при написании, потом поставим

SIZE = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

volume = 60
change_difficult = 0
select_lang = 0
DIFFICULTY = ['easy', 'normal', 'hard', 'cheat']
LANGUAGES = ['en', 'ru']
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

    def draw(self, x, y, button_image, message=None, action=None, font_size=50):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y - 5))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text,
                        (x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2) - 5))
            if clicked[0]:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text,
                        (x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))


class SystemButton:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, image, message, font_size=50):
        screen.blit(pygame.transform.scale(load_image(image), (self.width, self.height)), (x, y))
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')
        screen.blit(text,
                    (x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))


def show_menu(screen, clock):
    """ Отрисовка самого меню """
    menu_background = load_image('background.jpg')
    show = True
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    scores_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(WIDTH - 500, HEIGHT - 500, 'btn_menu.png', 'Start game', game_cycle)
        settings_btn.draw(WIDTH - 500, HEIGHT - 410, 'btn_menu.png', 'Settings', settings)
        scores_btn.draw(WIDTH - 500, HEIGHT - 320, 'btn_menu.png', 'Scores', scores)
        exit_btn.draw(WIDTH - 500, HEIGHT - 140, 'btn_menu.png', 'Exit', terminate)
        help_btn.draw(WIDTH - 500, HEIGHT - 230, 'btn_menu.png', 'Help', help_menu)
        pygame.display.update()
        clock.tick(60)


def start_menu():
    running = True
    clock = pygame.time.Clock()
    show_menu(screen, clock)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tick = clock.tick()
        pygame.display.flip()
    pygame.quit()


def game_cycle():
    """ Отрисовка самого меню """
    menu_background = load_image('background_2.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #     logging.warning('game exit by keys')
                    show = False

        screen.blit(menu_background, (0, 0))
        pygame.display.update()


def settings():
    settings_background = load_image('background_2.jpg')
    volume_btn = SystemButton(400, 135)
    difficulty_btn = SystemButton(400, 135)
    language_btn = SystemButton(400, 135)
    change_lang_btn = Button(40, 40)
    quiet_btn = Button(40, 15)
    loud_btn = Button(40, 40)
    easier_btn = Button(40, 15)
    harder_btn = Button(40, 40)
    about_btn = Button(400, 135)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
        screen.blit(settings_background, (0, 0))
        volume_btn.draw(460, 50, 'settings_btns.png', f'Volume {volume}%')
        difficulty_btn.draw(460, 200, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}", 40)
        language_btn.draw(460, 350, 'settings_btns.png', f'Language: {LANGUAGES[select_lang]}')
        about_btn.draw(460, 500, 'settings_btns.png', 'About', about_widget)

        quiet_btn.draw(500, 110, 'minus_btn.png', '', quiet_volume)
        loud_btn.draw(780, 95, 'plus_btn.png', '', loud_volume)
        easier_btn.draw(500, 260, 'minus_btn.png', '', reduce_difficult)
        harder_btn.draw(780, 245, 'plus_btn.png', '', increase_difficult)
        change_lang_btn.draw(780, 395, 'plus_btn.png', '', change_language)

        pygame.display.update()


def scores():
    menu_background = load_image('background_2.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #     logging.warning('game exit by keys')
                    show = False

        screen.blit(menu_background, (0, 0))
        pygame.display.update()


def help_menu():
    about = load_image('background_2.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False

        screen.blit(about, (0, 0))
        pygame.display.update()


def loud_volume():
    global volume
    volume_btn = SystemButton(400, 135)
    volume += 10
    volume_btn.draw(460, 200, 'settings_btns.png', f'Volume {volume}%')
    if volume == 110:
        volume = 0


def quiet_volume():
    global volume
    volume_btn = SystemButton(400, 135)
    volume -= 10
    volume_btn.draw(460, 200, 'settings_btns.png', f'Volume {volume}%')
    if volume == -10:
        volume = 100


def increase_difficult():
    global change_difficult
    difficulty_btn = SystemButton(400, 135)
    change_difficult += 1
    if change_difficult == 4:
        change_difficult = 0
        difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")
    difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")


def reduce_difficult():
    global change_difficult
    difficulty_btn = SystemButton(400, 135)
    change_difficult -= 1
    difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")
    if change_difficult == -1:
        change_difficult = 3


def change_language():
    global select_lang
    language_btn = SystemButton(400, 135)
    select_lang += 1
    if select_lang == 2:
        select_lang = 0
        language_btn.draw(460, 510, 'settings_btns.png', f'Language: {LANGUAGES[select_lang % 2]}')
    language_btn.draw(460, 510, 'settings_btns.png', f'Language: {LANGUAGES[select_lang % 2]}')


def about_widget():
    about = pygame.transform.scale(load_image('about.png'), (700, 600))
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False

        screen.blit(about, (300, 40))
        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    start_menu()
