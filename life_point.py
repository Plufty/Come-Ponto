import pygame
from point import Point
class LifePoint(Point):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/life.png").convert_alpha()
        self.sound = pygame.mixer.Sound("sounds/vida.ogg")
        super().__init__(x, y)