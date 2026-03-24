import pygame
import random

class Powerup(pygame.sprite.Sprite):
    '''
    Class for the powerup thing or something
    '''
    def __init__(self, y, screen): 
        super().__init__()
        self.image = pygame.image.load(f"assets/Car ({random.randint(1,5)}).png").convert_alpha()  # load a random one of the five sprites for the car
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        
            
    def kill(self):
        super().kill()
            
