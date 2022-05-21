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
                if graph.adding_edge:
                    if graph.check_clicked_vertex_while_adding_edge(pos):
                        graph.adding_edge = False
                else:
                    graph.check_clicked_vertex(pos)

            clicked_button = buttons_bar.get_clicked_button(event)
            if clicked_button:
                if clicked_button.text == "LOAD GRAPH":
                    file_path = buttons_bar.choose_file_dialog()
                    graph.load_graph_from_file(file_path)
                if clicked_button.text.endswith("DIRECTED"):
                    if clicked_button.color == Colors.RED:
                        graph.change_directing(True)
                        clicked_button.change_text("DIRECTED")
                        clicked_button.color = Colors.GREEN
                        clicked_button.hover_color = Colors.DARK_GREEN
                    elif clicked_button.color == Colors.GREEN:
                        graph.change_directing(False)
                        clicked_button.change_text("UNDIRECTED")
                        clicked_button.color = Colors.RED
                        clicked_button.hover_color = Colors.DARK_RED
                if clicked_button.text.endswith("WEIGHTED"):
                    if clicked_button.color == Colors.RED:
                        graph.change_weighted(True)
                        clicked_button.change_text("WEIGHTED")
                        clicked_button.color = Colors.GREEN
                        clicked_button.hover_color = Colors.DARK_GREEN
                    elif clicked_button.color == Colors.GREEN:
                        graph.change_weighted(False)
                        clicked_button.change_text("UNWEIGHTED")
                        clicked_button.color = Colors.RED
                        clicked_button.hover_color = Colors.DARK_RED
                if clicked_button.text == "ADD NODE":
                    pos = pygame.mouse.get_pos()
                    if len(graph.vertex_dict) > 0:
                        num = max(graph.vertex_dict.keys()) + 1
                    else:
                        num = 1
                    graph.add_vertex(num, pos)
                    graph.check_clicked_vertex(pos)
                if clicked_button.text == "ADD EDGE":
                    graph.adding_edge = True

        pygame.display.update()
