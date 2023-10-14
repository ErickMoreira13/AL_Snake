import pygame
from random import randint


class Apple:
    # Construtor
    def __init__(self, screen, scale): # Transformação linear
        self.scale = scale
        self.rect = pygame.Rect(0, 0, self.scale, self.scale)
        self.color = 'red'

        x = randint(self.scale, screen.get_width() - self.scale)
        y = randint(self.scale, screen.get_height() - self.scale)

        while y < self.scale * 3 + self.scale:
            y = randint(self.scale, screen.get_height()-self.scale)

        self.rect.topleft = (x//self.scale * self.scale, y//self.scale * self.scale)

    # Desenha na tela a posição 
    def drawPosition(self, screen): # Vetor no espaço
        font = pygame.font.Font(None, self.scale+3)
        font_pos = font.render(f'Apple pos: ({self.rect.x/self.scale:.0f}, {(self.rect.y - self.scale*3)/self.scale:.0f})', True, ('white'))
        font_rect = font_pos.get_rect()
        font_rect.bottomright = (screen.get_width() - 2, self.scale*3 - 2)
        screen.blit(font_pos, font_rect)

    # Desenha a maçã
    def drawApple(self, screen, difficultyMenu):
        if difficultyMenu.lower() == 'facil':
            pygame.draw.rect(screen, self.color, self.rect)
    
    # Muda a escala
    def changeScale(self, scale):
        self.scale = scale
        self.rect.w = self.scale
        self.rect.h = self.scale

    # Define uma posição aleatória
    def random_position(self, screen):
        x = randint(self.scale, screen.get_width() - self.scale)
        y = randint(self.scale, screen.get_height() - self.scale)

        while y < self.scale * 3 + self.scale:
            y = randint(self.scale, screen.get_height()-self.scale)

        self.rect.topleft = (x//self.scale * self.scale, y//self.scale * self.scale)


# Classe da maçã normal/vermelha    
class AppleRed(Apple):
    # Construtor
    def __init__(self, screen, scale: int = 20, color='red'):
        super().__init__(screen, scale)
        self.color = color
        self.special = False

    def reset(self, scale):
        self.scale = scale
        self.changeScale(self.scale)


# Classe da maçã especial 
class AppleGreen(Apple):
    # Construtor
    def __init__(self, screen, scale: int = 20, color='green'):
        super().__init__(screen, scale)
        self.scales = [20, 30, 40, 50]
        self.onGrid = False
        self.special = True
        self.canCollide = False
        self.color = color
        self.timer = 0
        self.maxTimer = 15

        # Gerando proxima escala
        self.otherScale = self.scales[randint(0, len(self.scales)-1)]

        while self.otherScale == self.scale:
            self.otherScale = self.scales[randint(0, len(self.scales)-1)]

    # Desenhando/exibindo a maçã especial na tela
    def drawApple(self, screen, ActiveItemMenu):
        if ActiveItemMenu.lower() == 'dificil' and self.onGrid:
            pygame.draw.rect(screen, self.color, self.rect)

    # Resetando a escala 
    def reset(self, scale):
        self.scale = scale
        self.changeScale(self.scale)
        self.canCollide = False
        self.onGrid = False
        self.timer = 0

        # Resendo a proxima escala para não ser a padrão
        self.otherScale = self.scales[randint(0, len(self.scales)-1)]

        while self.otherScale == self.scale:
            self.otherScale = self.scales[randint(0, len(self.scales)-1)]

    # Atualização do tempo do jogo em relação a maçã especial (coldown para a maçã especial)
    def updateTimer(self, screen):
        if not self.onGrid:
            self.timer += 0.1

            if self.timer > self.maxTimer:
                # self.timer = 0
                self.onGrid = True
                self.canCollide = True
                self.random_position(screen)

        if self.onGrid and self.timer < 30:
            self.timer += 0.1

            if self.timer > 30:
                self.timer = 0
                self.onGrid = False
                self.canCollide = False

    # Muda a escala do jogo ao comer a maçã especial
    def changeGameScale(self, screen, snake, apple, game):
        self.timer = 0
        self.onGrid = False
        self.canCollide = False
        self.changeScale(self.otherScale)
        snake.changeScale(self.otherScale)
        apple.changeScale(self.otherScale)
        apple.random_position(screen)
        game.setScale(self.otherScale)

        # Gerando proxima escala
        self.otherScale = self.scales[randint(0, len(self.scales)-1)]

        while self.otherScale == self.scale:
            self.otherScale = self.scales[randint(0, len(self.scales)-1)]