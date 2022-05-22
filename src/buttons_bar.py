import tkinter
import tkinter.filedialog

import pygame
from .constants import *
from .button import Button
from .graph import Graph


class ButtonsBar:

    def __init__(self):
        self.color = Colors.DARK_GREY
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 5)
        self.buttons = [
            Button("LOAD GRAPH", 15, (10, 5, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            Button("SCALE", 15, (170, 5, 70, 40), Colors.BLUE, Colors.BLUE),
            Button("+", 30, (240, 5, 40, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("-", 30, (280, 5, 40, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("UNDIRECTED", 15, (10, 55, 150, 40), Colors.RED, Colors.DARK_RED),
            Button("ADD NODE", 15, (10, 105, 150, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("ADD EDGE", 15, (170, 105, 150, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("UNWEIGHTED", 15, (170, 55, 150, 40), Colors.RED, Colors.DARK_RED),

            Button("DFS", 15, (350, 35, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            Button("BFS", 15, (350, 85, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            # undirected
            Button("BRIDGES", 15, (510, 35, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            Button("ARTIC. POINTS", 15, (510, 85, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            # WEIGHTED
            Button("DIJKSTRA", 15, (670, 35, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            # weighted and undirected
            Button("MST", 15, (830, 35, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
            # directed
            Button("SCC", 15, (830, 85, 150, 40), Colors.GREEN, Colors.DARK_GREEN),
        ]

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, self.rect)
        for button in self.buttons:
            button.draw(win)

    def get_clicked_button(self, event: pygame.event) -> Button:
        for button in self.buttons:
            if button.is_mouse(event):
                return button

    def update_algo_buttons_state(self, graph: Graph):
        for button in self.buttons:
            if button.text == "BRIDGES" or button.text == "ARTIC. POINTS":
                if not graph.directing:
                    button.active = True
                else:
                    button.active = False
            if button.text == "DIJKSTRA":
                if graph.weighted:
                    button.active = True
                else:
                    button.active = False
            if button.text == "MST":
                if graph.weighted and not graph.directing:
                    button.active = True
                else:
                    button.active = False
            if button.text == "SCC":
                if graph.directing:
                    button.active = True
                else:
                    button.active = False


    @staticmethod
    def choose_file_dialog():
        t = tkinter.Tk()
        t.withdraw()
        file_path = tkinter.filedialog.askopenfilename(parent=t)
        t.destroy()
        return file_path
