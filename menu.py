import pygame

class Menu:
    def __init__(self, screen, title, options, x, y):
        self.__screen = screen
        self.__title = title
        self.__options = options
        self.__x, self.__y = x, y
        self.__font = pygame.font.Font(None, 74)  # Define a fonte e tamanho do texto
        self.__selected = 0  # Inicialmente, a primeira opção é selecionada
        self.__running = True
        self.__background = pygame.image.load("img/Menu.jpeg").convert_alpha()  # Carrega a imagem do fundo
        self.__background = pygame.transform.scale(self.__background, screen.get_size())  # Redimensiona a imagem para o tamanho da tela

    def draw_text(self, text, font, color, x, y, shadow=True):
        if shadow:
            shadow_color = (0, 0, 0)
            shadow_surface = font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
            self.__screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.__screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.__screen.blit(self.__background, (0, 0))  # Desenha a imagem de fundo na tela
            self.draw_text(self.__title, self.__font, (255, 255, 255), self.__screen.get_width() / 2, 100)  # Renderiza o título

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"  # Se o jogador fechar a janela, sai do jogo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"  # Se o jogador apertar esc volta para o menu anterior
                    if event.key == pygame.K_UP:
                        self.__selected = (self.__selected - 1) % len(self.__options)  # Move para cima na lista de opções
                    elif event.key == pygame.K_DOWN:
                        self.__selected = (self.__selected + 1) % len(self.__options)  # Move para baixo na lista de opções
                    elif event.key == pygame.K_RETURN:
                        return self.__options[self.__selected].lower().replace(" ", "_")  # Retorna a opção selecionada

            # Renderiza e desenha as opções na tela
            for i, option in enumerate(self.__options):
                color = (255, 255, 255) if i == self.__selected else (100, 100, 100)  # Cor da opção selecionada
                self.draw_text(option, self.__font, color, self.__screen.get_width() / 2, 200 + i * 100)

            pygame.display.flip()  # Atualiza a tela

    def pause(self):
        self.__options = ["Resume Game", "Exit"]
        self.__selected = 0

        while self.__running:
            self.__screen.blit(self.__background, (0, 0))  # Desenha a imagem de fundo na tela
            self.draw_text("Paused", self.__font, (255, 255, 255), self.__screen.get_width() / 2, 100)  # Renderiza o título

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.__selected = (self.__selected - 1) % len(self.__options)
                    if event.key == pygame.K_DOWN:
                        self.__selected = (self.__selected + 1) % len(self.__options)
                    if event.key == pygame.K_RETURN:
                        if self.__selected == 0:
                            return "resume"
                        elif self.__selected == 1:
                            return "exit"

            for i, option in enumerate(self.__options):
                color = (255, 255, 255) if i == self.__selected else (100, 100, 100)
                self.draw_text(option, self.__font, color, self.__screen.get_width() / 2, 200 + i * 100)

            pygame.display.flip()
