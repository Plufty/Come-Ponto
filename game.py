import pygame
import random
from player import Player
from point_old import Point
from score import Score
from menu import Menu
from life_point import LifePoint
from speed_point import SpeedPoint
from score_point import ScorePoint

class Game:
    def __init__(self, screen, difficulty, x, y):
        self.__screen = screen  # Atribui a tela passada como parâmetro
        self.__clock = pygame.time.Clock()  # Cria um relógio para controlar o tempo
        self.__background = pygame.image.load("img/Fundo.jpg").convert_alpha()  # Carrega a imagem do jogador
        self.__background = pygame.transform.scale(self.__background, screen.get_size())  # Redimensiona a imagem para o tamanho da tela
        self.__running = True  # Flag para manter o jogo rodando
        self.__paused = False  # Flag para controlar o estado de pausa do jogo
        self.__x, self.__y = x, y
        self.__player = Player(screen, x, y)  # Cria a instância do jogador
        self.__points = pygame.sprite.Group()  # Cria um grupo para os pontos
        self.__score = Score(screen)  # Cria a instância do score
        self.__point_spawn_time = 0  # Inicializa o contador de tempo para criar novos pontos
        self.__lives = 3  # Define o número inicial de vidas
        self.__font = pygame.font.Font(None, 36)  # Configura a fonte para desenhar texto na tela
        self.__difficulty = difficulty        
        self.__speedChance = 0.1 #chance de vir raio

        # Carrega o arquivo de áudio de fundo
        pygame.mixer.music.load("sounds/music.ogg")

        # Definindo a velocidade de queda dos pontos baseado na dificuldade
        if self.__difficulty == 'easy':
            self.__point_speed = 2.5 
        elif self.__difficulty == 'medium':
            self.__point_speed = 3.75
        else:  # 'hard'
            self.__point_speed = 5

    def run(self):
        pygame.mixer.music.play(-1)  # -1 significa loop infinito para tocar a música sempre

        while self.__running:
            if not self.__paused:
                self.__clock.tick(60)  # Limita o loop do jogo a 60 FPS
                self.events()  # Trata os eventos (como teclas pressionadas)
                self.update()  # Atualiza o estado do jogo
                self.draw()  # Desenha todos os elementos na tela
                if self.__lives <= 0:
                    pygame.mixer.music.stop()
                    self.game_over()  # Verifica se o jogador perdeu todas as vidas
                    return 'exit_to_menu'  # Retorna ao menu principal ao dar game over
                elif self.__difficulty == 'easy' and self.__score.getScore() >= 50:
                    self.victory() #chama a vitória
                    return 'exit_to_menu'  # Retorna ao menu principal ao dar game over
                elif self.__difficulty == 'medium' and self.__score.getScore() >= 100:
                    self.victory() #chama a vitória
                    return 'exit_to_menu'  # Retorna ao menu principal ao dar game over
                elif self.__difficulty == 'hard' and self.__score.getScore() >= 1:
                    self.victory() #chama a vitória
                    return 'exit_to_menu'  # Retorna ao menu principal ao dar game over

            else:
                menu = Menu(self.__screen, "Paused", ["Resume Game", "Restart", "Exit"], self.__x, self.__y)
                action = menu.pause()  # Exibe o menu de pausa e espera uma ação
                if action == 'resume':
                    self.__paused = False  # Retoma o jogo
                elif action == 'restart':
                    return 'restart'  # Reinicia o jogo
                elif action == 'exit':
                    pygame.mixer.music.stop()
                    return 'exit_to_menu'  # Retorna ao menu principal

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False  # Encerra o jogo se o jogador fechar a janela
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__paused = True  # Pausa o jogo se o jogador pressionar ESC

    def update(self):
        self.__player.update()  # Atualiza o estado do jogador
        self.__points.update(self.__point_speed)  # Atualiza o estado dos pontos

        self.__point_spawn_time += 1  # Incrementa o contador de tempo para criar novos pontos
        if self.__point_spawn_time > 60:
            self.__point_spawn_time = 0  # Reseta o contador
            number = random.random()
            if number < 0.15:  # 10% de chance de criar um ponto de vida
                if number < self.__speedChance and self.__score.getScore() > 10:
                    self.__speedChance = self.__speedChance * 0.5 #diminui a chance de vir raio
                    print(self.__speedChance)
                    new_point = SpeedPoint(self.__x, self.__y)
                else:
                    new_point = LifePoint(self.__x, self.__y)
            else:
                new_point = ScorePoint(self.__x, self.__y)
            self.__points.add(new_point)  # Adiciona o novo ponto ao grupo de pontos

        for point in pygame.sprite.spritecollide(self.__player, self.__points, True):
            if isinstance(point, LifePoint):
                self.__lives += 1  # Aumenta uma vida se for um ponto de vida
            elif isinstance(point, SpeedPoint):
                self.__player.speedy()  # Aumenta a velocidade dos pontos se for um
            else:
                self.__score.increase()
            point.sound.play()

        for point in self.__points:
            if point.rect.bottom >= self.__screen.get_height():
                point.kill()  # Remove o ponto se ele atingir o fundo da tela
                if not isinstance(point, LifePoint) and not isinstance(point, SpeedPoint):
                    point.damage.play()
                    self.__lives -= 1  # Diminui uma vida se for um ponto normal

    def draw(self):
        self.__screen.blit(self.__background, (0, 0))  # Desenha a imagem de fundo na tela
        self.__player.draw(self.__screen)  # Desenha o jogador na tela
        self.__points.draw(self.__screen)  # Desenha os pontos na tela
        self.__score.draw(self.__screen)  # Desenha o score na tela

        shadow_color = (0, 0, 0)
        shadow_surface = self.__font.render(f"Lives: {self.__lives}", True, shadow_color)
        shadow_rect = shadow_surface.get_rect(topleft=((20, 52)))
        self.__screen.blit(shadow_surface, shadow_rect)

        lives_surface = self.__font.render(f"Lives: {self.__lives}", True, (255, 192, 203))  # Cria o texto de vidas       
        self.__screen.blit(lives_surface, (18, 50))  # Desenha o texto de vidas na tela

        pygame.display.flip()  # Atualiza a tela

    def game_over(self):
        pygame.mixer.music.load("sounds/perdeu.ogg")
        pygame.mixer.music.play(1)
        game_over = self.__font.render("Game Over", True, (255, 0, 0))  # Cria o texto de Game Over
        game_over_rect = game_over.get_rect(center=(self.__screen.get_width() / 2, 200 + 1 * 100))  # Centraliza o texto
        self.__screen.blit(game_over, game_over_rect)  # Desenha o texto de Game Over na tela
        pygame.display.flip()  # Atualiza a tela
        pygame.time.wait(5000)  # Espera 5 segundos antes de retornar ao menu principal
        pygame.mixer.music.stop()
        # Retorna ao menu principal após o game over

    def victory(self):
        pygame.mixer.music.load("sounds/ganhou.ogg")
        pygame.mixer.music.play(1)
        victory = self.__font.render("Parabéns amiguinho, você é 10!", True, (255, 192, 203))  # Cria o texto de Game Over
        victory_rect = victory.get_rect(center=(self.__screen.get_width() / 2, 200 + 1 * 100))  # Centraliza o texto
        self.__screen.blit(victory, victory_rect)  # Desenha o texto de Game Over na tela
        pygame.display.flip()  # Atualiza a tela
        pygame.time.wait(12000)  # Espera 5 segundos antes de retornar ao menu principal
        pygame.mixer.music.stop()
        # Retorna ao menu principal após o game over
