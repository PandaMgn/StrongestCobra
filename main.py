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
FPS = 30

BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strongest Cobra")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()

game_state = State.MENU
player = None

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False

    all_sprites.update()
    screen.fill(BLACK)
    
    match game_state:
        case State.MENU:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game_state = State.GAME
                player = Player(200, 200, 1, screen)
        case State.GAME:
            player.updatePosition(pygame.key.get_pressed())
            print(f"x: {player.x}, y: {player.y}")
        case State.END:
            pass



    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()