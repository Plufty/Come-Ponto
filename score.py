import pygame

class Score:
    def __init__(self, screen):
        self.__font = pygame.font.Font(None, 36)
        self.__score = 0
        self.__screen = screen
        self.__background = pygame.image.load("img/rainbow.png").convert_alpha()  # Carrega a imagem do arco-íris
        self.__background = pygame.transform.scale(self.__background, (self.__screen.get_width() *0.15, self.__screen.get_height()*0.12))  # Redimensiona a imagem para caber no texto

    def increase(self):
        self.__score += 1

    def getScore(self):
        return self.__score

    def draw(self, screen, shadow=True):
        text = f"Score: {self.__score}"
        text_surface = self.__font.render(text, True, (255, 192, 203))
        text_rect = text_surface.get_rect(topleft=(18, 20))
        screen.blit(self.__background, text_rect)  # Desenha o fundo do arco-íris
        if shadow:
            shadow_color = (0, 0, 0)
            shadow_surface = self.__font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(topleft=(20, 22))
            self.__screen.blit(shadow_surface, shadow_rect)
        self.__screen.blit(text_surface, text_rect)

