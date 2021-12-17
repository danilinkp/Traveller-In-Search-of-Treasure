import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('pygame-project')
    pygame.display.set_mode((100, 100), pygame.FULLSCREEN)
    running = True
    x = y = 0
    clock = pygame.time.Clock()
    balls = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tick = clock.tick()
        pygame.display.flip()
    pygame.quit()
