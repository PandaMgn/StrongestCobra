import pygame
import random
import enum

import menu
from player import Player
import gameworld

class State(enum.Enum):
    MENU = enum.auto()
    GAME = enum.auto()
    END = enum.auto()


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
button_font = pygame.font.Font(None, 30)
start_screen = menu.Game_Screen(screen, title_font, subtitle_font, (255, 255, 255))


all_sprites = pygame.sprite.Group(Player((200, 200), 5))

game_state = State.MENU

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False


    match game_state:
        case State.MENU:
            menu.Game_Screen.draw_start_screen(start_screen)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game_state = State.GAME

        case State.GAME:
            all_sprites.update()
            all_sprites.draw(screen)
            screen.fill(BLACK)
            pass
        case State.END:
            pass

    pygame.display.flip()

pygame.quit()