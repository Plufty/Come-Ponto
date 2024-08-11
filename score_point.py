import pygame
from point import Point
class ScorePoint(Point):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/IceCream.png").convert_alpha()
        self.sound = pygame.mixer.Sound("sounds/comeu.ogg")
        self.damage = pygame.mixer.Sound("sounds/damage.ogg")
        super().__init__(x, y)