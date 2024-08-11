import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()  # Inicializa o Pygame
    x, y = 800, 600
    screen_size = (x, y)
    screen = pygame.display.set_mode((screen_size))  # Cria uma tela com dimensões 800x600 pixels
    pygame.display.set_caption("Sweet Unicorn: Rainbow Ice Cream Adventure")  # Define o título da janela do jogo
    # Carrega o arquivo de áudio de fundo
    pygame.mixer.music.load("sounds/menu.ogg")


    original_screen_size = screen_size #Salva a resolução original

    # Cria o menu principal com as opções Start Game, Settings e Exit
    main_menu = Menu(screen, "Main Menu", ["Start Game", "Settings", "Exit"], x, y)
    running = True
    
    pygame.mixer.music.play(-1)  # -1 significa loop infinito para tocar a música sempre
    while running:
        action = main_menu.run()  # Executa o menu principal e obtém a ação selecionada pelo jogador

        if action == 'start_game':
            # Se o jogador escolher Start Game, cria o menu de seleção de dificuldade
            difficulty_menu = Menu(screen, "Select Difficulty", ["Easy", "Medium", "Hard"], x, y)
            difficulty = difficulty_menu.run()  # Executa o menu de dificuldade e obtém a dificuldade selecionada

            if difficulty:
                if difficulty == "back": # Se o jogador apertar esc, retorna ao menu principal
                    continue
                # Se uma dificuldade foi selecionada, cria o jogo com a dificuldade escolhida
                game = Game(screen, difficulty, x, y)
                pygame.mixer.music.stop()
                result = game.run()  # Executa o jogo e obtém o resultado ao finalizar

                # Verifica o resultado do jogo
                if result == 'restart':
                    continue  # Reinicia o jogo se o jogador escolher reiniciar
                elif result == 'exit_to_menu':
                    pygame.mixer.music.load("sounds/menu.ogg")
                    pygame.mixer.music.play(-1)
                    continue  # Retorna ao menu principal se o jogador escolher sair para o menu
                else:
                    running = False  # Encerra o jogo se o jogador terminar completamente

        elif action == 'settings':# Menu de Configurações
            settings_menu = Menu(screen, "Settings", ["Resolution", "Fullscreen"], x, y)
            setting_action = settings_menu.run()  # Executa o menu de configurações e obtém a ação selecionada

            if setting_action == 'resolution':
                # Submenu para escolher a resolução
                resolution_menu = Menu(screen, "Resolution", ["800x600", "1024x768", "1280x1024", "1920x1080"], x, y)
                resolution_action = resolution_menu.run()

                if resolution_action == '800x600':
                    x, y = 800, 600
                    screen_size = (x, y)
                elif resolution_action == '1024x768':
                    x, y = 1024, 768
                    screen_size = (x, y)
                elif resolution_action == '1280x1024':
                    x, y = 1280, 1024
                    screen_size = (x, y)
                elif resolution_action == '1920x1080':
                    x, y = 1920, 1080
                    screen_size = (x, y)

                screen = pygame.display.set_mode(screen_size)  # Altera a resolução da tela
                main_menu = Menu(screen, "Main Menu", ["Start Game", "Settings", "Exit"], x, y)

            elif setting_action == 'fullscreen':
                # Toggle para tela cheia
                fullscreen = not screen.get_flags() & pygame.FULLSCREEN
                screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN if fullscreen else 0)

        elif action == 'exit':
            pygame.mixer.music.stop()
            running = False  # Encerra o loop principal se o jogador escolher sair do jogo

    pygame.quit()  # Finaliza o Pygame ao sair do loop principal

if __name__ == "__main__":
    main()  # Executa a função principal ao iniciar o script
