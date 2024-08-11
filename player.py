import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, speed=5):
        super().__init__()  # Inicializa a classe base Sprite
        self.__screen = screen
        self.__speed = speed
        self.image_right = pygame.image.load("img/UnicornD.png").convert_alpha()  # Sprite para movimento para a direita
        self.image_left  = pygame.image.load("img/UnicornE.png").convert_alpha()   # Sprite para movimento para a esquerda
        self.image_idle  = pygame.image.load("img/UnicornF1.png").convert_alpha()   # Sprite para quando estiver parado
        self.image = self.image_idle  # Começa com a sprite de parado
        self.__x, self.__y = x, y #Resolução da tela pra delimitar o espaço do player
        self.rect = self.image.get_rect()  # Obtém o retângulo da superfície para manipulação de posição
        self.rect.centerx = self.__screen.get_width() // 2  # Define a posição horizontal inicial do jogador no centro da tela
        self.rect.bottom = self.__screen.get_height() - int(self.__screen.get_height() * 0.05)

    def update(self):
        keys = pygame.key.get_pressed()  # Obtém o estado de todas as teclas do teclado

        if keys[pygame.K_LEFT]:  # Se a tecla esquerda estiver pressionada
            self.rect.x -= self.__speed  # Move o jogador 5 pixels para a esquerda
            self.image = self.image_left  # Altera para a sprite de movimento para a esquerda

        elif keys[pygame.K_RIGHT]:  # Se a tecla direita estiver pressionada
            self.rect.x += self.__speed  # Move o jogador 5 pixels para a direita
            self.image = self.image_right  # Altera para a sprite de movimento para a direita

        else:
            self.image = self.image_idle  # Se não estiver pressionando nenhuma tecla de movimento, usa a sprite de parado

        
        # Limita o movimento do jogador às bordas da tela
        if self.rect.left < 0:  # Se o jogador ultrapassar a borda esquerda
            self.rect.left = 0  # Define a posição na borda esquerda
        if self.rect.right > self.__x:  # Se o jogador ultrapassar a borda direita (considerando a largura da tela como 800 pixels)
            self.rect.right = self.__x  # Define a posição na borda direita
    def speedy(self):
        self.__speed +=10

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Desenha a superfície do jogador na tela na posição do retângulo
