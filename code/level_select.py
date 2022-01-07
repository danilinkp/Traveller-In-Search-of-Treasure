import os
import sys
from itertools import product

import pygame

pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
colors = {'Black': pygame.Color('Black'),
          'White': pygame.Color('White'),
          'Red': pygame.Color('Red'),
          'Blue': pygame.Color('Blue')}

running = True
MENU_BTN_SOUND = pygame.mixer.Sound('sounds/menu_btn.wav')

def load_image(name, dictor='images', colorkey=None):
    fullname = os.path.join(dictor, name)
    # если файл не существует   , то выходим
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

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
    screen.fill((0, 0, 0))
   # pygame.Rect(1, 1, size[0] - 2, size[1] - 2)
    #screen.fill(pygame.Color('red'), pygame.Rect(30, 30, 280, 150))
    level_1 = Button(89 * 1.9, 67 * 1.9)
    level_1.draw(89, 67,  f'', 'level_btn.png')
    level_2 = Button(89 * 1.9, 67 * 1.9)
    level_2.draw(350, 67, f'', 'level_btn.png')
    level_3 = Button(89 * 1.9, 67 * 1.9)
    level_3.draw(89, 67, f'', 'level_btn.png')
    level_4 = Button(89 * 1.9, 67 * 1.9)
    level_4.draw(89, 67, f'', 'level_btn.png')
    level_5 = Button(89 * 1.9, 67 * 1.9)
    level_5.draw(89, 67, f'', 'level_btn.png')
    level_6 = Button(89 * 1.9, 67 * 1.9)
    level_6.draw(89, 67, f'', 'level_btn.png')
    level_7 = Button(89 * 1.9, 67 * 1.9)
    level_7.draw(89, 67, f'', 'level_btn.png')
    level_8 = Button(89 * 1.9, 67 * 1.9)
    level_8.draw(89, 67, f'', 'level_btn.png')


    pygame.display.flip()
