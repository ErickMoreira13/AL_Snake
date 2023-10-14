import pygame


class Snake:
    # Construtor
    def __init__(self, x, y, screen: pygame.Surface, scale: int = 20, color: str = 'grey'): #Constructor
        self.scale = scale
        self.bodyPositions = [(x, y), (x + self.scale, y), (x + self.scale*2, y)]
        self.square = pygame.Surface((self.scale-1, self.scale-1))
        self.square.fill(color)
        self.direction = 3  # Para esquerda
        self.score_rect = pygame.Rect(0, 0, screen.get_width(), self.scale*3)
        self.speed = self.scale
        self.isDead = False
        self.score = 0
        self.picked_upSpecial = False
        self.soundEat = pygame.mixer.Sound("snake/audios/comer.mp3")
        self.soundEat.set_volume(0.5)

    # Desenhando o bodyPositions da cobra na tela
    def drawBody (self, screen):
        for position in self.bodyPositions:
            screen.blit(self.square, position)

    # Desenhando a tela de score
    def drawScore (self, screen):
        font = pygame.font.Font(None, self.scale+3)
        font_score = font.render(f'Score: {self.score}', True, ('white'))
        font_rect = font_score.get_rect()
        font_rect.topleft = (2, 2)
        pygame.draw.rect(screen, ((93,93,93)), self.score_rect)
        screen.blit(font_score, font_rect)

        # Fornecendo a posição 
        font_snake_pos = font.render(f'Snake pos: ({self.bodyPositions[0][0]/20:.0f}, {(self.bodyPositions[0][1] - self.scale*3)/20:.0f})', True, ('white'))
        font_rect = font_snake_pos.get_rect()
        font_rect.bottomleft = (2, self.score_rect.bottom - 2)
        screen.blit(font_snake_pos, font_rect)

    # Atribuindo uma nova escala
    def changeScale(self, scale):
        self.scale = scale
        self.speed = scale
        self.score_rect.h = self.scale*3
        self.square = pygame.Surface((self.scale-1, self.scale-1))
        self.square.fill('grey')
        self.bodyPositions[0] = (self.bodyPositions[0][0]//self.scale*self.scale,self.bodyPositions[0][1]//self.scale*self.scale)

        for i in range(1, len(self.bodyPositions)):
            self.bodyPositions[i] = (self.bodyPositions[i][0]//self.scale*self.scale, self.bodyPositions[i][1]//self.scale*self.scale)

    # Movendo/atualizando as posições do bodyPositions da cobra
    def updateBody (self):
        if not self.isDead:
            for i in range(len(self.bodyPositions) -1, 0, -1):
                self.bodyPositions[i] = (self.bodyPositions[i-1][0], self.bodyPositions[i-1][1])

    # Movendo a cabeça da cobra usando plano cartesiano (x, y) 
    def moveSnake (self):
        # Para cima 
        if self.direction == 0:
            self.bodyPositions[0] = (self.bodyPositions[0][0], self.bodyPositions[0][1] - self.speed)
        
        # Para direita
        if self.direction == 1:
            self.bodyPositions[0] = (self.bodyPositions[0][0] + self.speed, self.bodyPositions[0][1])
        
        # Para baixo
        if self.direction == 2:
            self.bodyPositions[0] = (self.bodyPositions[0][0], self.bodyPositions[0][1] + self.speed)
       
        # Para esquerda
        if self.direction == 3:
            self.bodyPositions[0] = (self.bodyPositions[0][0] - self.speed, self.bodyPositions[0][1])

    # Atribuindo colisão com base na tela 
    def collision (self, screen, game, difficultyMenu):
        if difficultyMenu.lower() == 'facil':
            if self.bodyPositions[0][0] < self.scale:
                self.bodyPositions[0] = (screen.get_width() - self.scale, self.bodyPositions[0][1])

            if self.bodyPositions[0][0] + self.scale > screen.get_width():
                self.bodyPositions[0] = (self.scale, self.bodyPositions[0][1])

            if self.bodyPositions[0][1] < self.score_rect.bottom + self.scale:
                self.bodyPositions[0] = (self.bodyPositions[0][0], screen.get_height()-self.scale)

            if self.bodyPositions[0][1] + self.scale > screen.get_height():
                self.bodyPositions[0] = (self.bodyPositions[0][0], self.score_rect.bottom + self.scale)

        else:
            if self.bodyPositions[0][0] < self.scale:
                self.isDead = True
                for i in range(0, len(self.bodyPositions)):
                    self.bodyPositions[i] = (self.bodyPositions[i][0] + self.scale, self.bodyPositions[i][1])
            
            if self.bodyPositions[0][0] + self.scale > screen.get_width():
                self.isDead = True
                for i in range(0, len(self.bodyPositions)):
                    self.bodyPositions[i] = (self.bodyPositions[i][0] - self.scale, self.bodyPositions[i][1])

            if self.bodyPositions[0][1] < self.score_rect.bottom + self.scale:
                self.isDead = True
                for i in range(0, len(self.bodyPositions)):
                    self.bodyPositions[i] = (self.bodyPositions[i][0], self.bodyPositions[i][1] + self.scale)
            
            if self.bodyPositions[0][1] + self.scale > screen.get_height():
                self.isDead = True
                for i in range(0, len(self.bodyPositions)):
                    self.bodyPositions[i] = (self.bodyPositions[i][0], self.bodyPositions[i][1] - self.scale)

            if self.isDead:
                game.setActiveState(3) # Game-Over
                self.speed = 0 
                self.square.fill('red') 

    # Colisão com o prórpio bodyPositions (corpo) da cobra
    def collisionBody(self, game):
        for i in range(1, len(self.bodyPositions)):
            if self.bodyPositions[0][0] == self.bodyPositions[i][0] and self.bodyPositions[0][1] == self.bodyPositions[i][1]:
                game.setActiveState(3) # Game-Over
                self.speed = 0
                self.square.fill('red')
                self.isDead = True

    # Colisão com a maçã
    def collisionApple (self, apple, screen, difficultyMenu):
        # Maça verde
        if apple.special:
            if difficultyMenu.lower() == 'dificil' and apple.canCollide:
                if self.bodyPositions[0][0] == apple.rect.x and self.bodyPositions[0][1] == apple.rect.y:
                    self.score += 1
                    self.bodyPositions.append(self.bodyPositions[-1])
                    self.picked_upSpecial = True
                    self.soundEat.play()

        else:
            # Maça vermelha
            if self.bodyPositions[0][0] == apple.rect.x and self.bodyPositions[0][1] == apple.rect.y:
                self.score += 1
                self.bodyPositions.append((self.bodyPositions[-1]))
                apple.random_position(screen)
                self.soundEat.play()
                
    # Reset da cobra
    def reset(self, screen, scale):
        self.scale = scale
        self.speed = self.scale
        self.score = 0
        self.direction = 3 # Para esquerda
        self.isDead = False
        self.score_rect.h = self.scale*3
        self.square = pygame.Surface((self.scale-1, self.scale-1))
        self.square.fill('grey')
        self.picked_upSpecial =  False
        x = screen.get_width() // 2 // self.scale * self.scale
        y = screen.get_height() // 2 // self.scale * self.scale
        self.bodyPositions = [(x, y), (x + self.scale, y), (x + self.scale*2, y)]




