import pygame
import background
import car
import random
import time
import powerup
import math

class Game_World:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.score = 0

        #lanes for cars and stuff
        self.lanes = []
        
        #background stuff
        None
        
    def spawn_lane(self, speed):
        
        #starting lanes
        if len(self.lanes) <= 1:
            lane = Lane(self.screen, 400, speed)
            self.lanes.append(lane)
            lane = Lane(self.screen, 100, speed)
            self.lanes.append(lane)
            lane = Lane(self.screen, -200, speed)
            self.lanes.append(lane)
            lane = Lane(self.screen, -500, speed)
            self.lanes.append(lane)    
            
        cars = []
        
        while len(self.lanes) < 4: #four lanes at a time, three on screen, one up there
            lane = Lane(self.screen, -200, speed)
            self.lanes.append(lane)
            new_car = lane.spawn_car_initial()
            cars.append(new_car)


        for lane in self.lanes:
            lane.update()
            new_car = lane.spawn_car()
            cars.append(new_car)
            
            if lane.rect.top > self.h:
                lane.kill()
                self.lanes.remove(lane)
                
        return cars

    def spawn_powerup(self):

        powerups = []


        if random.random() < 0.01:
            new_powerup = powerup.Powerup(self.screen, "assets/Wings.png")
            powerups.append(new_powerup)

        return powerups

  
    def reset(self):
        self.spawn_timer = 0
        for lane in self.lanes:
            lane.kill()
        self.lanes = []
        self.score = 0

class Lane(pygame.sprite.Sprite):
    def __init__(self, screen, y, speed):
        super().__init__()
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.speed = speed
        self.spawn_timer = 251 #spawn a car immediatley
        self.direction = random.choice(["R", "L"])
        self.pos = y
        
        self.image = pygame.image.load("assets/Road.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.w/2, y)

    
    def spawn_car(self):
        self.spawn_timer += random.randint(0,4)
        if self.spawn_timer > (500) / math.pow(self.speed, 0.3):
            self.spawn_timer = 0
            new_car = car.Car(self.rect.y, self.screen, self.speed, self.direction)
            return new_car
        return None
    
    def spawn_car_initial(self):
        new_car = car.Car(self.rect.y, self.screen, self.speed, self.direction)
        new_car.rect.x = random.randint(0, self.w)
        return new_car
    
    def update(self):
        self.screen.blit(self.image, self.rect)

        
    