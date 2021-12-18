import logging
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


class Button:
    """ Класс кнопок для создания непосредственно самих конпок """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = MENU_INACTIVE_BTN_COLOR
        self.active_color = MENU_ACTIVE_BTN_COLOR

    def draw(self, x, y, message, action=None, font_size=50):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if clicked[0]:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        # вот это надо буедт попраавить ибо не отрисовывает в нужном месте текст
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')

        screen.blit(text, (x + text.get_width() // 2 - 20, y + text.get_height() // 2))


def show_menu(screen, clock):
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
        start_btn.draw(300, 200, 'Start game', game_cycle)
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
    menu_background = pygame.image.load('images/background_2.jpg')
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



if __name__ == '__main__':
    start_menu()
