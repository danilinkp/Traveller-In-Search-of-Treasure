import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, image):
        super().__init__()
        # print(size)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        # print(image)
        # self.image = pygame.Surface((size, size))

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class AnimatedTile(Tile):
    def __init__(self, pos, size, sprites):
        self.frames = sprites
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        super().__init__(pos, size, self.image)
        self.frames = sprites
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
