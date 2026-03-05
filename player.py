import pygame

class Player:
    x = None
    y = None
    velocity = 0
    screen = None
    moveCooldown = None

    def __init__(self, x, y, velocity, screen):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.screen = screen
    
    def updatePosition(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_DOWN]:
            self.y -= self.velocity
        