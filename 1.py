import logging
from time import sleep
import os
import sys
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
    """ Класс кнопок для создания непосредственно самих конпок """

    def __init__(self, width, height):
        self.width = width
        self.height = height

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


def text_write(x, y, message, font_size=50):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, 'white')
    screen.blit(text,
                (x + ((400 - text.get_width()) // 2), y + ((135 - text.get_height()) // 2)))


def show_menu(screen, clock):
    """ Отрисовка самого меню """
    menu_background = load_image('background.jpg')
    show_menu_f = True
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    scores_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    while show_menu_f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(WIDTH - 500, HEIGHT - 500, 'Start game', 'btn_menu.png', game_cycle)
        settings_btn.draw(WIDTH - 500, HEIGHT - 410, 'Settings', 'btn_menu.png', settings)
        scores_btn.draw(WIDTH - 500, HEIGHT - 320, 'Scores', 'btn_menu.png', scores)
        exit_btn.draw(WIDTH - 500, HEIGHT - 140, 'Exit', 'btn_menu.png', terminate)
        help_btn.draw(WIDTH - 500, HEIGHT - 230, 'Help', 'btn_menu.png', help_menu)
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
    name = FunctionCallDrawing('images/background_2.jpg', [(460, 100), (460, 100)],
                               [[(80, 80), 'Story mode', 'btn.png', story_mode],
                                [(730, 80), 'PVP mode', 'btn.png', pvp_mode]])
    name.run()


def story_mode():
    name = FunctionCallDrawing('images/background_5.jpg', [(540, 150), (460, 100), (460, 100)],
                               [[(360, 80), 'NEW GAME', 'btn.png', story_mode_new_game],
                                [(400, 260), 'STORE', 'btn.png', store_mode],
                                [(400, 400), 'HEROES', 'btn.png', pvp_mode]
                                ])
    name.run()


def story_mode_new_game():
    name = FunctionCallDrawing('images/for_nickname.jpg', [(380, 70)],
                               [[(880, 600), 'ok', 'btn.png', story_mode_new_game_select_heroes]])
    name.run()


def story_mode_new_game_select_heroes():
    name = FunctionCallDrawing('images/select_heroes.jpg', [(380, 70)],
                               [[(450, 620), 'select', 'btn.png', levels_show_menu]])
    name.run()


def levels_show_menu():
    name = FunctionCallDrawing('images/start_level.jpg', [(500, 100)],
                               [[(700, 560), 'start', 'btn.png', game]])
    name.run()


def pvp_mode():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               # потом нужно будет исправить
                               [[(145, 500), 'select', 'btn.png', pvp_mode_2],
                                [(515, 500), 'select', 'btn.png', pvp_mode_2],
                                [(885, 500), 'select', 'btn.png', pvp_mode_2]
                                ])
    name.run()


def pvp_mode_2():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               # потом нужно будет исправить
                               [[(145, 500), 'start', 'btn.png', play_pvp_mode],
                                [(515, 500), 'start', 'btn.png', play_pvp_mode],
                                [(885, 500), 'start', 'btn.png', play_pvp_mode]
                                ])
    name.run()


def game():
    pass


def play_pvp_mode():
    pass


def store_mode():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'select', 'btn.png', buy_mage],
                                [(515, 500), 'select', 'btn.png', buy_warrior],
                                [(885, 500), 'select', 'btn.png', buy_archer]
                                ])
    name.run()


def buy_mage():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


def buy_warrior():
    """ Отрисовка самого меню """
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


def buy_archer():
    """ Отрисовка самого меню """
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


class FunctionCallDrawing:
    def __init__(self, backgroundimage, w_h, name_coords_fun):
        self.back_im = backgroundimage
        self.w_h = w_h
        self.name_coords_fun = name_coords_fun
        self.buttons = []
        self.running = True

    def run(self):
        menu_background = pygame.image.load(self.back_im)

        for i in self.w_h:
            self.buttons.append(Button(i[0], i[1]))
            print(i)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            screen.blit(menu_background, (0, 0))
            for i in range(len(self.buttons)):
                self.buttons[i].draw(self.name_coords_fun[i][0][0],
                                     self.name_coords_fun[i][0][1],
                                     self.name_coords_fun[i][1],
                                     self.name_coords_fun[i][2],
                                     self.name_coords_fun[i][3])
            pygame.display.update()


def settings():
    settings_background = load_image('for_settings.jpg')
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
        quiet_btn.draw(480, 120, '', 'minus_btn.png', quiet_volume)
        loud_btn.draw(760, 105, '', 'plus_btn.png', loud_volume)
        text_write(440, 60, f"Volume: {volume}%")
        easier_btn.draw(480, 260, '', 'minus_btn.png', reduce_difficult)
        harder_btn.draw(760, 245, '', 'plus_btn.png', increase_difficult)
        text_write(440, 200, f"Difficult: {DIFFICULTY[change_difficult]}", 40)
        change_lang_btn.draw(760, 405, '', 'plus_btn.png', change_language)
        text_write(440, 360, f"Language: {LANGUAGES[select_lang]}")
        about_btn.draw(445, 500, 'About', 'settings_btns.png', about_widget)
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
    about = load_image('background_5.jpg')
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
    volume += 10
    if volume == 110:
        volume = 0
        text_write(440, 60, f"Volume: {volume}%")
    text_write(440, 60, f"Volume: {volume}%")


def quiet_volume():
    global volume
    volume -= 10
    if volume == -10:
        volume = 100
        text_write(440, 60, f"Volume: {volume}%")
    text_write(440, 60, f"Volume: {volume}%")


def increase_difficult():
    global change_difficult
    change_difficult += 1
    if change_difficult == 4:
        change_difficult = 0
        text_write(440, 200, f"Difficult: {DIFFICULTY[change_difficult]}", 40)
    text_write(440, 200, f"Difficult: {DIFFICULTY[change_difficult]}", 40)


def reduce_difficult():
    global change_difficult
    change_difficult -= 1
    text_write(440, 200, f"Difficult: {DIFFICULTY[change_difficult]}", 40)
    if change_difficult == -1:
        change_difficult = 3


def change_language():
    global select_lang
    select_lang += 1
    if select_lang == 2:
        select_lang = 0
        text_write(440, 360, f"Language: {LANGUAGES[select_lang % 2]}")
    text_write(440, 360, f"Language: {LANGUAGES[select_lang % 2]}")


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
