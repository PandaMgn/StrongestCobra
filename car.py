import pygame
import random

class Car:
    '''
    Class for the enemy thing or smth
    '''
    def __init__(self, pos, screen, direction = "R"): 
        super().__init__()
        self.image = pygame.image.load(f"assets/Car ({random.randint(1,3)}).png").convert()  # load a random one of the five sprites for the car
        self.image = pygame.transform.scale(self.image, (50,50))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = random.randint(5,10)
        self.direction = direction
        self.screen_w, self.screen_h = screen.get_size()
        self.screen = screen

    def create(self):
        if self.direction == "R": # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
            self.rect = self.image.get_rect(center=(
                random.randint(20, self.screen_w - 20), #x
                random.randint(50, 50),)) #y

    def Update(self):
        # position is shifted in y-direction only, based on the sprite's speed
        self.rect.move_ip(0, self.speed)
        # if off screen, kill/destroy the object
        if self.rect.top > self.screen_h:
            self.kill()
    

    '''
    def move_enemy(self):
        if self.direction == "R": #if the car moves from left to right
            self.rect.move_ip(self.x+self.speed, self.y)

        else: #if the car goes the other diretion than that one up there
            self.rect.move_ip(self.x-self.speed, self.y)
    '''