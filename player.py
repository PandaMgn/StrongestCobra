import pygame
import math

class Player(pygame.sprite.Sprite):
    pos = None
    velocity = None
    def __init__(self, pos, velocity):
        super(Player, self).__init__()
        #self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        self.image = pygame.image.load("assets/CoolCobra.png")
        pygame.draw.polygon(self.image, (0, 100, 240), [(60, 0), (120, 120), (0, 120)])
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pos
        self.velocity = velocity
    
    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_DOWN]:
            dy += 1
        
        hypotenuse = math.hypot(dx, dy)
        if hypotenuse > 0:
            dx = dx/hypotenuse*self.velocity
            dy = dy/hypotenuse*self.velocity
            self.rect.move_ip(dx, dy)
