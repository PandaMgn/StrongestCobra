import pygame
import math

class Player(pygame.sprite.Sprite):
    '''class for the player, handles movement and stuff'''
    pos = None
    velocity = None


    abs_posy = 0
    score = 0
    def __init__(self, pos, velocity, screen, normal_image, ability_image):
        super(Player, self).__init__()
        
        self.normal_image = pygame.image.load(normal_image).convert_alpha()
        self.fly_image = pygame.image.load(ability_image).convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (100,100))
        self.fly_image = pygame.transform.scale(self.fly_image, (140,140))
        self.image = self.normal_image
        
        self.screen = screen
        self.rect = self.image.get_rect(center=pos)
        self.rect.center = (self.screen.get_width()/2, self.screen.get_height()/1.5) #start game at bottom middle
        self.mask = pygame.mask.from_surface(self.image)

        self.health = 5
        self.invincible = False
        self.powerup_duration = 0 #just invincibility
        
        self.ability_rect = pygame.Rect(0, 0, 250, 250)
        self.ability_cd = 0
    
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
        if keys[pygame.K_w]:
            self.score += 5
        
        self.abs_posy -= dy
        self.score = max(self.score, self.abs_posy//300)


        self.rect.move_ip(dx, dy)
        self.ability_rect.center = self.rect.center
            
        self.rect.clamp_ip(self.screen.get_rect())
        
        if self.invincible:
            self.powerup_duration -= 1
            if self.powerup_duration <= 0:
                self.invincible = False
                self.image = self.normal_image
                self.image.set_alpha(255)
                
        if self.ability_cd > 0:
            self.ability_cd -= 1
        
        
    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.powerup_duration = 180
            self.image.set_alpha(100) # transparent if invincible
        
    def fly(self):
        self.score += 5
        self.abs_posy += 1500
        self.invincible = True
        self.powerup_duration = 180
        self.image = self.fly_image
        
        
    def ability(self, carGrp):
        destroyed = 0
        if self.ability_cd <= 0:
            print("ready")
            for car in carGrp:
                if self.ability_rect.colliderect(car.rect):
                    car.kill()
                    destroyed += 1
        if destroyed > 0:
            self.score += destroyed*10
            self.abs_posy += destroyed*3000
            self.health += destroyed
            self.ability_cd = 300
            
            
            
            
    def reset(self):
        self.rect.center = (self.screen.get_width()/2, self.screen.get_height()/1.5) #start game at bottom middle
        self.health = 5
        self.invincible = False
        self.powerup_duration = 0
        self.abs_posy = 0
        self.score = 0
        self.image = self.normal_image
        
            
