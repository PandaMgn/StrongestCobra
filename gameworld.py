import pygame
import background
import car
import random


class Game_World:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        
        #lanes for cars and stuff
        self.lanes = []
        
        #background stuff
        None
        
    def spawn_lane(self):
        
        #starting lanes
        if len(self.lanes) <= 1:
            lane = Lane(self.screen, 400)
            self.lanes.append(lane)
            lane = Lane(self.screen, 100)
            self.lanes.append(lane)
            lane = Lane(self.screen, -200)
            self.lanes.append(lane)
            lane = Lane(self.screen, -500)
            self.lanes.append(lane)    
            
               
        while len(self.lanes) < 4: #four lanes at a time, three on screen, one up there
            lane = Lane(self.screen, -200)
            self.lanes.append(lane)

        cars = []

        for lane in self.lanes:
            lane.update()
            new_car = lane.spawn_car()
            cars.append(new_car)
            
            if lane.rect.top > self.h:
                lane.kill()
                self.lanes.remove(lane)
                
        return cars
    
    def reset(self):
        self.spawn_timer = 0
        for lane in self.lanes:
            lane.kill()
        self.lanes = []

class Lane(pygame.sprite.Sprite):
    def __init__(self, screen, y):
        super().__init__()
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.speed = random.randint(3,6)
        self.spawn_timer = 0
        self.direction = random.choice(["R", "L"])
        self.pos = y
        
        self.image = pygame.image.load("assets/Road.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.w/2, y)
    
    def spawn_car(self):
        self.spawn_timer += random.randint(0,4)
        if self.spawn_timer > 250:
            self.spawn_timer = 0
            new_car = car.Car(self.rect.y, self.screen, self.speed, self.direction)
            return new_car
        return None
    
    def update(self):
        self.screen.blit(self.image, self.rect)

        
    