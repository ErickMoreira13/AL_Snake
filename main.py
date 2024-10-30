import pygame 
from pygame.locals import *
from classes.Apple import *
from classes.Game import *
from classes.Menu import *
from classes.Snake import *


pygame.init()

clock = pygame.time.Clock()
tick = 10 # Passagem de tempo

# Dimensões da tela do jogo
W = 600
H = 600

# Escala principal usada
SCALE = 20

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake game')

# Fontes usadas
fonts: dict = {
    '70': pygame.font.Font(None, 70),
    '40': pygame.font.Font(None, 40),
    '30': pygame.font.Font(None, 30),
    '25': pygame.font.Font(None, 25),
}

# Opções do menu principal
MenuItens = ['Iniciar', 'Informacoes', 'Sair']
menu: Menu = Menu(W//2, H//2 - 100, MenuItens)

# Dificuldades do jogo
difficultyItens = ['Facil', 'Medio', 'Dificil']
difficultyMenu = Menu(W//2, H//2 - 100, difficultyItens)

# Atribuindo os estados do jogo para controle
game: Game = Game(['menu', 'dificuldade', 'jogando', 'gameover', 'pause', 'informacoes'], SCALE)

# Atribuindo o estado de jogo atual
gameState = game.getActiveState()

# Criando snake
snake: Snake = Snake(W//2, H//2, screen, game.getScale())

# Declarando as maças
apple: AppleRed = AppleRed(screen, game.getScale())
specialApple: AppleGreen = AppleGreen(screen, game.getScale())


done = False # Controle do programa (run or dont run)
death = 0

# Runing 
while not done:
    clock.tick(tick) #Passando o tempo...
    screen.fill('black') #Preenchendo a tela com a cor 'black'
    
    #Verificando os eventos
    for event in pygame.event.get():
        # Fechar janela
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if gameState == 'menu':
                if event.key in [K_w, K_UP]:
                    menu.setItemActive(1)

                if event.key in [K_s, K_DOWN]:
                    menu.setItemActive(0)

                if event.key == K_RETURN:
                    item: str = menu.getItemActive()
                    item = item.lower()

                    if item == 'iniciar':
                        death = 0
                        game.setActiveState(1) # Dificuldade
                        game.setScale(SCALE)
                        snake.reset(screen, game.getScale())
                        apple.reset(game.getScale())
                        specialApple.reset(game.getScale())
                        apple.random_position(screen)

                    if item == 'informacoes':
                        game.setActiveState(5)
                    
                    if item == 'sair':
                        done = True
            
            if gameState == 'dificuldade':
                if event.key in [K_w, K_UP]:
                    difficultyMenu.setItemActive(1)

                if event.key in [K_s, K_DOWN]:
                    difficultyMenu.setItemActive(0)
                
                if event.key == K_RETURN:
                    game.setActiveState(2)

                if event.key == K_ESCAPE:
                    game.setActiveState(0)

            if gameState == 'jogando':
                if event.key in [K_w, K_UP] and snake.direction != 2:
                    # Para cima
                    snake.direction = 0

                if event.key in [K_d, K_RIGHT] and snake.direction != 3:
                    # Para direita 
                    snake.direction = 1

                if event.key in [K_s, K_DOWN] and snake.direction != 0:
                    # Para baixo
                    snake.direction = 2

                if event.key in [K_a, K_LEFT] and snake.direction != 1:
                    # Para Para esquerda
                    snake.direction = 3

                # Pausar no meio do jogo
                if event.key == K_p:
                    game.setActiveState(4) 

            if gameState == 'pause':
                # Voltar para o jogo
                if event.key == K_p:
                    game.setActiveState(2)
                
                # Voltar para o menu
                if event.key == K_ESCAPE:
                    game.setActiveState(0)
            
            if gameState == 'gameover':
                # Voltar para o menu principal
                if event.key == K_ESCAPE:
                    game.setActiveState(0)
                    snake.reset(screen, game.getScale())

            if gameState == 'informacoes':
                # Voltar para o menu principal
                if event.key == K_ESCAPE: 
                    game.setActiveState(0)
                    
    gameState = game.getActiveState()


    if gameState == 'menu':
        menu.drawItens(fonts["70"], screen, itemActiveColor = 'yellow')

    if gameState == 'dificuldade':
        difficultyMenu.drawItens(fonts["70"], screen, itemActiveColor = 'yellow')

        font_back = fonts["40"].render('[Esc] Voltar para o menu', True, ('white'))
        font_rect = font_back.get_rect()
        font_rect.topleft = (10, H - 30)
        screen.blit(font_back, font_rect)

    if gameState == 'jogando':
        snake.updateBody()
        snake.moveSnake()
        snake.collision(screen, game, difficultyMenu.getItemActive())
        snake.collisionBody(game)
        snake.collisionApple(apple, screen, difficultyMenu.getItemActive())
        snake.collisionApple(specialApple, screen, difficultyMenu.getItemActive())
        

        specialApple.updateTimer(screen)

        if snake.picked_upSpecial:
            specialApple.changeGameScale(screen,snake, apple, game)
            snake.picked_upSpecial = not snake.picked_upSpecial

        for i in range(0, len(snake.bodyPositions)):
            if snake.bodyPositions[i][0] == apple.rect.x and snake.bodyPositions[i][1] == apple.rect.y:
                x = randint(apple.scale, screen.get_width() - apple.scale)
                y = randint(apple.scale, screen.get_height() - apple.scale)

                while y < apple.scale * 3 + apple.scale:
                    y = randint(apple.scale, screen.get_height()-apple.scale)

                apple.rect.topleft = (x//apple.scale * apple.scale, y//apple.scale * apple.scale)

        apple.drawApple(screen, difficultyMenu.getItemActive())
        specialApple.drawApple(screen, difficultyMenu.getItemActive())
        snake.drawBody(screen)

        game.drawGrids(screen)

        snake.drawScore(screen)
        apple.drawPosition(screen)

    if gameState == 'pause':
        apple.drawApple(screen, difficultyMenu.getItemActive())
        snake.drawBody(screen)

        game.drawGrids(screen)

        snake.drawScore(screen)
        apple.drawPosition(screen)

        font_pause = fonts["70"].render(f'Pause - {difficultyMenu.getItemActive()}', True, ('white'))
        font_rect = font_pause.get_rect()
        font_rect.center = (W//2, H//2)
        screen.blit(font_pause, font_rect)

        font_back = fonts["40"].render('[Esc] Voltar para o menu', True, ('white'))
        font_rect = font_back.get_rect()
        font_rect.topleft = (10, H - 30)
        screen.blit(font_back, font_rect)

    if gameState == 'gameover':
        if snake.isDead:
            if death == 0:
                pygame.mixer.Sound("snake/audios/game-over.mp3").play()
                death = 1
            
            snake.drawBody(screen)

            game.drawGrids(screen)

            snake.drawScore(screen)
            apple.drawPosition(screen)
             
            font_gameover = fonts["70"].render('Fim de Jogo', True, ('white'), ('black'))
            font_rect = font_gameover.get_rect()
            font_rect.center = (W//2, H//2)
            screen.blit(font_gameover, font_rect)

            font_back = fonts["40"].render('[Esc] Voltar para o menu', True, ('white'))
            font_rect = font_back.get_rect()
            font_rect.topleft = (10, H - 30)
            screen.blit(font_back, font_rect)

    if gameState == 'informacoes':
        # Texto de informações sobre o projeto
        texto = [
            "Esse é um jogo que aborda de forma lúdica matrizes, baseado",
            "no jogo clássico da serpente. Contém três dificuldades: fácil,",
            "médio e difícil.",
            " ",
            "Fácil: jogo normal;",
            "",
            "Médio: maçã fica invisivel, recebendo apenas a informação de",
            "sua posicao;",
            "",
            "Difícil: analogo a dificuldade medio, porém há tambem uma",
            "maçã especial que pode redimensionar o campo da serpente,",
            "podendo aumentar ou diminuir."
        ]

        count = 25

        for linha in texto:
            font_info = fonts["25"].render(linha, True, ('white'))
            font_rect = font_info.get_rect()
            font_rect.topleft = (25, count)
            screen.blit(font_info, font_rect)
            count += 25
            
        font_back = fonts["40"].render('[Esc] Voltar para o menu', True, ('white'))
        font_rect = font_back.get_rect()
        font_rect.topleft = (10, H - 30)
        screen.blit(font_back, font_rect)
        
    #Atualizando a tela antes do fim  do laço de repetição
    pygame.display.update()        
                
print('Fim do programa')
