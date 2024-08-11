import pygame
import random

class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.__x, self.__y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, x - 20)
        self.rect.y = 0

    def update(self, point_speed):
        self.rect.y += point_speed
        if self.rect.top > self.__y:
            self.kill()
