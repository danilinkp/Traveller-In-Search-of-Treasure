import pygame

pygame.init()
pygame.display.set_caption('pygame-project')
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)

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

    def draw(self, x, y, message):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos[0] < x + self.width) and (y < mouse_pos[1] < y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if clicked:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        # вот это надо буедт попраавить ибо не отрисовывает в нужном месте текст
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, 'white')
        text_x = x + 10
        text_y = y + 10
        screen.blit(text, (text_x, text_y))


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
        start_btn.draw(300, 200, 'Start game')
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


if __name__ == '__main__':
    start_menu()
