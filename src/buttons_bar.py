import tkinter
import tkinter.filedialog

import pygame
from .constants import *
from .button import Button


class ButtonsBar:

    def __init__(self):
        self.color = Colors.DARK_GREY
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 5)
        self.buttons = [
            Button("LOAD GRAPH", 15, (20, 5, 280, 40), Colors.GREEN, Colors.DARK_GREEN),
            Button("UNDIRECTED", 15, (10, 55, 150, 40), Colors.RED, Colors.DARK_RED),
            Button("ADD NODE", 15, (10, 105, 150, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("ADD EDGE", 15, (170, 105, 150, 40), Colors.BLUE, Colors.DARK_BLUE),
            Button("UNWEIGHTED", 15, (170, 55, 150, 40), Colors.RED, Colors.DARK_RED),
        ]

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, self.rect)
        for button in self.buttons:
            button.draw(win)

    def get_clicked_button(self, event: pygame.event) -> Button:
        for button in self.buttons:
            if button.is_mouse(event):
                return button

    @staticmethod
    def choose_file_dialog():
        t = tkinter.Tk()
        t.withdraw()
        file_path = tkinter.filedialog.askopenfilename(parent=t)
        t.destroy()
        return file_path
