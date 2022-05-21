import sys
import pygame
from constants import *


def main():

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        win.fill(Colors.GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.update()
