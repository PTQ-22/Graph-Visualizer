import sys
import pygame
from .constants import *
from .buttons_bar import ButtonsBar
from .graph import Graph


def main():

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    buttons_bar = ButtonsBar()
    graph = Graph()

    while True:
        clock.tick(FPS)
        win.fill(Colors.GREY)

        buttons_bar.draw(win)
        graph.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            clicked_button = buttons_bar.get_clicked_button(event)
            if clicked_button:
                if clicked_button.text == "Load Graph":
                    file_path = buttons_bar.choose_file_dialog()
                    graph.load_graph_from_file(file_path)

        pygame.display.update()
