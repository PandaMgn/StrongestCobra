import pygame
import random
import math

class Car(pygame.sprite.Sprite):
    '''
    Class for the enemy thing or something
    '''
    def __init__(self, y, screen, speed, direction): 
        super().__init__()
        self.image = pygame.image.load(f"assets/Car ({random.randint(1,5)}).png").convert_alpha()  # load a random one of the five sprites for the car
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = direction
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        
        if direction == "R":
            self.rect.x = -self.rect.width
            self.rect.y = y
        else:
            self.image = pygame.transform.flip(self.image, True, False) #flip cause it gotta face L direction
            self.rect.x = self.screen_w
            self.rect.y = y
                    
    def update(self):
        dx = 0
        if self.direction == "R": #if the car moves from left to right
            dx += self.speed
        else:#if the car goes the other diretion than that one up there
            dx -= self.speed
        self.rect.move_ip(dx, 0)    
            
        if self.rect.right < 0 or self.rect.left > self.screen_w:
            self.kill()
            
    def kill(self):
        super().kill()
            
