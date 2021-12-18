import pygame

class Button:
    def __init__(self, x, y):
        pass

def show_menu(screen, clock):
    menu_background = pygame.image.load('maxresdefault.jpg')
    start_btn = Button(300, 70)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        #     start_btn.draw(300, 200, 'Start game')
        pygame.display.update()
        clock.tick(60)


def start_menu():
    pygame.init()
    pygame.display.set_caption('pygame-project')
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
    running = True
    x = y = 0
    clock = pygame.time.Clock()
    show_menu(screen, clock)
    balls = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tick = clock.tick()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_menu()
