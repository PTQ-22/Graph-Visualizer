import random
from typing import Tuple, List
from collections import defaultdict
from .constants import *
import pygame


class Vertex:

    RADIUS = 30
    LINE_SIZE = 5

    def __init__(self, number: int, pos: Tuple[int, int]):
        self.number = number
        self.rect = pygame.Rect(pos[0] - self.RADIUS, pos[1] - self.RADIUS, 2*self.RADIUS, 2*self.RADIUS)
        self.color = Colors.BLACK
        font = pygame.font.Font('freesansbold.ttf', 40)
        self.text = font.render(str(self.number), True, Colors.BLACK)

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, self.rect.center, self.RADIUS, self.LINE_SIZE)
        win.blit(self.text, self.text.get_rect(center=self.rect.center))


class Edge:

    def __init__(self):
        pass


class Graph:

    def __init__(self):
        self.adj_list = defaultdict(list)
        self.vertex_arr: List[Vertex] = []
        self.edge_arr = []

    def draw(self, win: pygame.Surface):
        for v in self.vertex_arr:
            v.draw(win)

    def add_vertex(self, num: int, pos: Tuple[int, int]):
        self.vertex_arr.append(Vertex(num, pos))

    def load_graph_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            try:
                n, m = file.readline().split()
                for i in range(int(m)):
                    a, b = file.readline().split()
                    a, b = int(a), int(b)
                    self.adj_list[a].append(b)
                    self.adj_list[b].append(a)

            except ValueError:
                print("Invalid file format")
                return

        for v in self.adj_list.keys():
            loop = True
            attempts = 0
            x, y = 0, 0
            while loop and attempts < 100:
                loop = False
                x = random.randint(Vertex.RADIUS, WIDTH - Vertex.RADIUS)
                y = random.randint(HEIGHT // 6 + Vertex.RADIUS, HEIGHT - Vertex.RADIUS)
                test_rect = pygame.Rect(x - Vertex.RADIUS, y - Vertex.RADIUS, 2*Vertex.RADIUS, 2*Vertex.RADIUS)
                for vertex in self.vertex_arr:
                    if test_rect.colliderect(vertex.rect):
                        loop = True
                        attempts += 1

            self.add_vertex(v, (x, y))
