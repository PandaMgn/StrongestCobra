'''
Author: Tony Meng and Alex Chen
blah blah blah
'''

import pygame
import random
import enum
import car
import menu
from player import Player
import gameworld

class State(enum.Enum):
    MENU = enum.auto()
    GAME = enum.auto()
    END = enum.auto()

#screen stuff
WIDTH = 540
HEIGHT = 960
FPS = 60
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strongest Cobra")
clock = pygame.time.Clock()

#screen stuff or smth
title_font = pygame.font.Font(None, 50)
subtitle_font = pygame.font.Font(None, 40)
start_screen = menu.Game_Screen(screen, title_font, subtitle_font)
game_screen = menu.Game_Screen(screen, title_font, subtitle_font)
end_screen = menu.Game_Screen(screen, title_font, subtitle_font)


all_sprites = pygame.sprite.Group(Player((200, 200), 5, screen))
carGrp = pygame.sprite.Group()


game_state = State.MENU
running = True
spawn_timer = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False

        '''
        if pygame.key.get_pressed()[pygame.K_1]:
            #  Create the new food
            new_food = car.Car((50, 50), screen, direction = "R")
            # Add new food to the food group and to the all sprites group
        '''


    match game_state:
        case State.MENU:
            start_screen.draw_start_screen()
            if start_screen.start_button.is_clicked(event):
                game_state = State.GAME

        case State.GAME:
            game_screen.draw_game_screen()
            if game_screen.ability_button.is_clicked(event) or pygame.key.get_pressed()[pygame.K_SPACE]:
                game_state = State.END #here for now prolly change later ig 
             
            spawn_timer += 1
            if spawn_timer > 15:
                spawn_timer = 0
                lane_y = random.choice([100, 400, 700])
                direction = random.choice(["R", "L"])
                new_car = car.Car(lane_y, screen, direction)
                carGrp.add(new_car)
                all_sprites.add(new_car)          
                                
            all_sprites.update()
            all_sprites.draw(screen)         

        case State.END:
            end_screen.draw_end_screen()
            if end_screen.replay_button.is_clicked(event):
                #reset player state each time
                all_sprites.empty()
                carGrp.empty()
                all_sprites.add(Player((200, 200), 5, screen))
                game_state = State.MENU

    pygame.display.flip()

pygame.quit()