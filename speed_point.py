import pygame
from point import Point
class SpeedPoint(Point):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/raio.png").convert_alpha()
        self.sound = pygame.mixer.Sound("sounds/speed.ogg")
        super().__init__(x, y)