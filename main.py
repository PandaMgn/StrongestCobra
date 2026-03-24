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


WIDTH = 640
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

player = Player((200, 200), 5, screen)
all_sprites = pygame.sprite.Group()
carGrp = pygame.sprite.Group()
gameworld = gameworld.Game_World(screen)
game_state = State.MENU
running = True

while running:
    clock.tick(FPS)
    
    space_pressed = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                space_pressed = True

            
    match game_state:
        case State.MENU:
            start_screen.draw_start_screen()
            if start_screen.start_button.is_clicked(event) or space_pressed:
                all_sprites.add(player)
                game_state = State.GAME

        case State.GAME:
            game_screen.draw_game_screen()
            
            
            '''here for testing'''
            if game_screen.ability_button.is_clicked(event) or space_pressed:
                gameworld.reset()
                all_sprites.empty()
                carGrp.empty()
                player.reset()
                game_state = State.END #here for now prolly change later ig 
             
            cars = gameworld.spawn_lane()
            for new_car in cars:
                if new_car:
                    carGrp.add(new_car)
                    all_sprites.add(new_car)
            
            difference_pov_y = 1 + max(HEIGHT/2 - player.rect.centery, 0)/30
            for sprite in all_sprites:
                sprite.rect.y += difference_pov_y #gravity
            for lane in gameworld.lanes:
                lane.rect.y += difference_pov_y

            if pygame.sprite.spritecollide(player, carGrp, False, pygame.sprite.collide_mask):
                gameworld.reset()
                all_sprites.empty()
                carGrp.empty()
                player.reset()
                game_state = State.END
    
              
            all_sprites.update()
            all_sprites.draw(screen)         

        case State.END:
            end_screen.draw_end_screen()
            if end_screen.replay_button.is_clicked(event) or space_pressed:
                game_state = State.MENU

    pygame.display.flip()

pygame.quit()