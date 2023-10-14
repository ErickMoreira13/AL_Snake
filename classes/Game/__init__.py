import pygame


class Game:
    # Construtor
    def __init__(self, state: list, scale: int = 20):
        self.state = state[:]
        self.activeState = self.state[0]
        self.scale = scale

    # Setar o estado ativo
    def setActiveState(self, state):
        self.activeState = self.state[state]

    # Pegar o estado ativo
    def getActiveState(self):
        return self.activeState
    
    # Setar a escala
    def setScale(self, scale):
        self.scale = scale

    # Pegar a escala
    def getScale(self):
        return self.scale
    
    # Desenhando o grid/matriz para localização 
    def drawGrids(self, screen):
        # Tela
        W: int = screen.get_width()
        H: int = screen.get_height()

        for i in range(4, W - self.scale): # linha horizontal
            pygame.draw.line(screen, ('white'), (self.scale, i*self.scale), (W, i*self.scale))

        for i in range(1, H-self.scale): # linha vertical
            pygame.draw.line(screen, ('white'), (i*self.scale, self.scale*3 + self.scale), (i*self.scale, H))

        font = pygame.font.Font(None, self.scale + 2)

        for c, i in enumerate(range(4, W-self.scale), start=1): # texto vertical
            font_number = font.render(f'{c}', True, ('white'))
            font_rect = font_number.get_rect()
            font_rect.topleft = (2, i*self.scale)
            screen.blit(font_number, font_rect)
        
        for c, i in enumerate(range(1, W-self.scale), start=1): # texto horizontal
            font_number = font.render(f'{c}', True, ('white'))
            font_rect = font_number.get_rect()
            font_rect.topleft = (i*self.scale, self.scale*3)
            screen.blit(font_number, font_rect)