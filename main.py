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

    
    screen.fill(BLACK)
    
    match game_state:
        case State.MENU:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game_state = State.GAME
        case State.GAME:
            all_sprites.update()
            pass
        case State.END:
            pass



    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()