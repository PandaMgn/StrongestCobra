'''
Author: Tony Meng and Alex Chen
blah blah blah
'''

import pygame
import random
import enum
import menu
from player import Player
import gameworld
from leaderboard import Leaderboard, LeaderboardUI
import math

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

all_sprites = pygame.sprite.Group()
carGrp = pygame.sprite.Group()
powerGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()


player_name = ""
player = Player((200, 200), 5, screen, "assets/CoolCobra.png", "assets/WingedCobra.png")


gameworld = gameworld.Game_World(screen)
game_state = State.MENU
running = True
powerupCountdown = 600

while running:
    clock.tick(FPS)
    
    enter_pressed = False
    space_pressed = False
    current_event = None

    for event in pygame.event.get():
        current_event = event
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                enter_pressed = True
            if event.key == pygame.K_SPACE:
                space_pressed = True
        
        if game_state == State.MENU:
            start_screen.name_select.handle_event(event)
        if game_state == State.END:
            leaderboard_ui.handle_input(event)
        #print(event)
            
    match game_state:
        case State.MENU:
            gameworld.reset()
            start_screen.draw_start_screen()


            if current_event != None:
                if start_screen.cobrabutton.is_clicked(current_event):
                    print("67")
                    playerGroup.add(player)
                    all_sprites.add(player)

                if start_screen.foxbutton.is_clicked(current_event):
                    player = Player((200, 200), 5, screen, "assets/CoolFox.png", "assets/WingedCobra.png")
                    playerGroup.add(player)
                    all_sprites.add(player)

                if start_screen.start_button.is_clicked(current_event) and len(playerGroup) == 1:
                    game_state = State.GAME

        case State.GAME:
            game_screen.draw_game_screen()
            
            #spawn stuff
            cars = gameworld.spawn_lane(math.pow(player.score, 0.7) + 3) # difficulty curvbe
            for new_car in cars:
                if new_car:
                    carGrp.add(new_car)
                    all_sprites.add(new_car)

            if len(powerGroup) < 1:
                powerupCountdown -= 1
                if powerupCountdown <= 0:
                    powerups = gameworld.spawn_powerup()
                    for powerup in powerups:
                        if powerup:
                            powerGroup.add(powerup)
                            all_sprites.add(powerup)
                            powerupCountdown = 600
            
            #gravity stuff
            difference_pov_y = 1 + max(HEIGHT/3 - player.rect.centery, 0)/10
            for sprite in all_sprites:
                sprite.rect.y += difference_pov_y
            for lane in gameworld.lanes:
                lane.rect.y += difference_pov_y
                           
            #collision stuff
            hits = pygame.sprite.spritecollide(player, carGrp, False, pygame.sprite.collide_mask)
            if hits:
                player.take_damage()
                if player.health == 0:
                    player.reset()
                    game_state = State.END
                    leaderboard = Leaderboard("leaderboard.db")
                    leaderboard.save_score(player_name, player.score)
                    print(leaderboard.get_top_scores(10))

                    leaderboard_ui = LeaderboardUI(screen, leaderboard, title_font, subtitle_font)
            

            hit = pygame.sprite.spritecollide(player, powerGroup, False, pygame.sprite.collide_mask)
            for powerup in hit:
                powerup.kill()
                player.fly()
                #player.fly()


            '''here for testing'''
            if current_event and game_screen.ability_button.is_clicked(current_event) or space_pressed:
                game_state = State.END #here for now prolly change later ig 
                leaderboard = Leaderboard("leaderboard.db")
                leaderboard.save_score(player_name, player.score)
                print(leaderboard.get_top_scores(10))

                leaderboard_ui = LeaderboardUI(screen, leaderboard, title_font, subtitle_font)

            #draw stuff
            all_sprites.update()
            all_sprites.draw(screen)
            screen.blit(player.image, player.rect)  # draw player LAST
                 
            game_screen.draw_game_menu(player.score, player.health)

        case State.END:
            end_screen.draw_end_screen(player.score)
            leaderboard_ui.draw()

            if current_event and end_screen.replay_button.is_clicked(current_event) or space_pressed:
                playerGroup.empty()
                all_sprites.empty()
                carGrp.empty()
                powerGroup.empty()
                game_state = State.MENU

    pygame.display.flip()

pygame.quit()