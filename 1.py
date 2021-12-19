import os
import sys

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


def show_menu():
    """ Отрисовка самого меню """
    menu_background = pygame.image.load('images/background.jpg')
    show_menu_f = True
    start_btn = Button(300, 70)
    while show_menu_f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(430, 200, 'Start game', 'btn.png', game_cycle)
        pygame.display.update()


def start_menu():
    running = True
    show_menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                               [[(145, 500), 'select', 'btn.png', play_pvp_mode],
                                [(515, 500), 'select', 'btn.png', play_pvp_mode],
                                [(885, 500), 'select', 'btn.png', play_pvp_mode]
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
                               [[(145, 500), 'select', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'select', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'select', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


def buy_archer():
    """ Отрисовка самого меню """
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'select', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'select', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'select', 'btn.png', story_mode_new_game_select_heroes]
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


if __name__ == '__main__':
    start_menu()
