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

        graph.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                graph.check_clicked_vertex(pos)

            clicked_button = buttons_bar.get_clicked_button(event)
            if clicked_button:
                if clicked_button.text == "LOAD GRAPH":
                    file_path = buttons_bar.choose_file_dialog()
                    graph.load_graph_from_file(file_path)
                if clicked_button.text.endswith("DIRECTED"):
                    graph.change_directing()
                    if clicked_button.color == Colors.RED:
                        clicked_button.change_text("DIRECTED")
                        clicked_button.color = Colors.GREEN
                        clicked_button.hover_color = Colors.DARK_GREEN
                    elif clicked_button.color == Colors.GREEN:
                        clicked_button.change_text("UNDIRECTED")
                        clicked_button.color = Colors.RED
                        clicked_button.hover_color = Colors.DARK_RED

        pygame.display.update()
