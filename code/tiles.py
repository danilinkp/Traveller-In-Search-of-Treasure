import pygame


class Tile(pygame.sprite.Sprite):
    """Класс, который отвечает за прорисовку карты"""

    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class AnimatedTile(Tile):
    """Класс, который реализует анимированные тайлы"""

    def __init__(self, pos, size, sprites):
        self.frames = sprites
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        super().__init__(pos, size, self.image)
        self.frames = sprites
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        """Непосредственно анимирует тайлы"""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
