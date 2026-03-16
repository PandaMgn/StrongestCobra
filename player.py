import pygame
import math

class Player(pygame.sprite.Sprite):
    pos = None
    velocity = None
    def __init__(self, pos, velocity, screen):
        super(Player, self).__init__()
        #self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        self.image = pygame.image.load("assets/CoolCobra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120,120))
        pygame.draw.polygon(self.image, (0, 100, 240), [(15,0), (30,30), (0,30)])
        self.rect = self.image.get_rect(center=pos)
        self.screen = screen
        self.rect.move_ip(self.screen.get_width()//8, self.screen.get_height()/1.5) #start game at bottom middle
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pos
        self.velocity = velocity
    
    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx -= 5
        if keys[pygame.K_UP]:
            dy -= 5
        if keys[pygame.K_RIGHT]:
            dx += 5
        if keys[pygame.K_DOWN]:
            dy += 5
        
        '''
        hypotenuse = math.hypot(dx, dy)
        if hypotenuse > 0:
            dx = dx/hypotenuse*self.velocity
            dy = dy/hypotenuse*self.velocity
        '''
        self.rect.move_ip(dx, dy)
            
        self.rect.clamp_ip(self.screen.get_rect())
