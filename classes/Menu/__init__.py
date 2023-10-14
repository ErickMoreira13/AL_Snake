import pygame


class Menu:
    # Construtor
    def __init__(self, x: int, y: int, itens: list):
        self.itens = itens[:]
        self.rect = pygame.Rect(x, y, 150, len(self.itens)*100)
        self.itemId = 0
        self.itemActive = self.itens[self.itemId]
        self.sound = pygame.mixer.Sound("snake/audios/menu_som.mp3")
        self.sound.set_volume(0.5)

    # Desenha/exibe os itens do menu na tela
    def drawItens(self, font: pygame.font.Font, screen, itemActiveColor: str = 'yellow'):
        for c, item in enumerate(self.itens):
            if self.itemActive == item:
                font_txt = font.render(f'{item}', True, (itemActiveColor))
                font_rect = font_txt.get_rect()
                font_rect.center = (self.rect.x - 10, self.rect.y + c * 65)
                screen.blit(font_txt, font_rect)
            else:
                font_txt = font.render(f'{item}', True, ('white'))
                font_rect = font_txt.get_rect()
                font_rect.center = (self.rect.x - 10, self.rect.y + c * 65)
                screen.blit(font_txt, font_rect)
    
    # Seta o item ativo 
    def setItemActive(self, direction):
        if direction == 0:
            self.itemId += 1
            self.sound.play()
            if self.itemId >= len(self.itens):
                self.itemId = 0

            self.itemActive = self.itens[self.itemId]
        else:
            self.itemId -= 1
            self.sound.play()
            if self.itemId < 0:
                self.itemId = len(self.itens) - 1

            self.itemActive = self.itens[self.itemId]
    
    # Pega o item ativo
    def getItemActive(self):
        return self.itemActive

