from typing import Tuple
import pygame

from src.constants import Colors

pygame.init()


class Button:

    def __init__(self, text: str, font_size: int, rect: Tuple[int, int, int, int],
                 color: Tuple[int, int, int], hover_color: Tuple[int, int, int]):
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.text = text
        self.text_obj = self.font.render(text, False, (0, 0, 0))
        self.text_rect = self.text_obj.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.active = True

    def draw(self, win: pygame.Surface):
        if self.active:
            pygame.draw.rect(win, self.current_color, self.rect)
        else:
            pygame.draw.rect(win, Colors.LIGHT_GREY, self.rect)
        win.blit(self.text_obj, self.text_rect)
        self.is_mouse(None)

    def is_mouse(self, event: pygame.event) -> bool:
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                return True
            return False
        self.current_color = self.color
        return False

    def change_text(self, new_text: str):
        self.text = new_text
        self.text_obj = self.font.render(new_text, False, (0, 0, 0))
        self.text_rect = self.text_obj.get_rect(center=
                                                (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2))