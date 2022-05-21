import math
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
        self.color = Colors.GREY
        self.border_color = Colors.BLACK
        font = pygame.font.Font('freesansbold.ttf', 40)
        self.text = font.render(str(self.number), True, Colors.BLACK)
        self.is_clicked = False

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, self.rect.center, self.RADIUS)
        if self.is_clicked:
            pygame.draw.circle(win, Colors.GREEN, self.rect.center, self.RADIUS, self.LINE_SIZE)
        else:
            pygame.draw.circle(win, self.border_color, self.rect.center, self.RADIUS, self.LINE_SIZE)
        win.blit(self.text, self.text.get_rect(center=self.rect.center))

    def get_pos(self):
        return self.rect.center


class Edge:

    SIZE = 5

    def __init__(self, a: Vertex = None, b: Vertex = None):
        self.color = Colors.BLACK
        self.directing = False
        self.start = a
        self.end = b

    def draw(self, win: pygame.Surface):
        if self.start and self.end:
            p1 = self.end.get_pos()
            p2 = self.start.get_pos()
            pygame.draw.line(win, self.color, p1, p2, self.SIZE)
            if self.directing:
                dist = 50

                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                rads = math.atan2(-dy, dx)
                rads %= 2 * math.pi
                degs = math.degrees(rads)

                new_x = p1[0] + (dist * math.cos(-rads))
                new_y = p1[1] + (dist * math.sin(-rads))

                self.draw_arrow(win, new_x, new_y, self.color, degs)

    def draw_arrow(self, win, x, y, color, angle=0.0):
        def rotate(pos, theta):
            cen = (0 + x, 0 + y)
            theta *= -(math.pi / 180)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            ret = ((cos_theta * (pos[0] - cen[0]) - sin_theta * (pos[1] - cen[1])) + cen[0],
                   (sin_theta * (pos[0] - cen[0]) + cos_theta * (pos[1] - cen[1])) + cen[1])
            return ret

        p0 = rotate((0 + x, -10 + y), angle)
        p1 = rotate((0 + x, 10 + y), angle)
        p2 = rotate((-20 + x, 0 + y), angle)

        pygame.draw.line(win, color, p0, p2, self.SIZE)
        pygame.draw.line(win, color, p1, p2, self.SIZE)


class Loop(Edge):

    def __init__(self, a: Vertex):
        super().__init__(a, a)

    def draw(self, win: pygame.Surface):
        p = self.start.get_pos()
        pygame.draw.circle(win, self.color, (p[0] + Vertex.RADIUS - 5, p[1] - Vertex.RADIUS + 5), 20, self.SIZE)
        if self.directing:
            self.draw_arrow(win, p[0] + Vertex.RADIUS + 10, p[1] - 15, self.color, 40)


class Graph:

    def __init__(self):
        self.adj_list_undirected = defaultdict(list)
        self.adj_list_directed = defaultdict(list)
        self.current_adj_list = self.adj_list_undirected
        self.vertex_dict: defaultdict[int, Vertex] = defaultdict()
        self.edge_arr: List[Edge] = []

        self.adding_edge = False
        self.adding_edge_first_v = None
        self.directing = False

    def draw(self, win: pygame.Surface):
        for e in self.edge_arr:
            e.draw(win)
        if self.adding_edge:
            pos = pygame.mouse.get_pos()
            if self.adding_edge_first_v:
                pygame.draw.line(win, Colors.BLACK, pos, self.adding_edge_first_v.get_pos(), Edge.SIZE)
            else:
                pygame.draw.line(win, Colors.BLACK, pos, (pos[0]+10, pos[1]+5), Edge.SIZE)
        for v in self.vertex_dict.values():
            v.draw(win)

    def update(self):
        for v in self.vertex_dict.values():
            if v.is_clicked:
                v.rect.center = pygame.mouse.get_pos()

    def change_directing(self, d: bool):
        if self.current_adj_list is self.adj_list_directed:
            self.current_adj_list = self.adj_list_undirected
        else:
            self.current_adj_list = self.adj_list_directed
        for e in self.edge_arr:
            e.directing = d
        self.directing = d

    def check_clicked_vertex(self, mouse_pos: Tuple[int, int]):
        for v in self.vertex_dict.values():
            if v.rect.collidepoint(mouse_pos):
                v.is_clicked = not v.is_clicked

    def check_clicked_vertex_while_adding_edge(self, mouse_pos: Tuple[int, int]) -> bool:
        for v in self.vertex_dict.values():
            if v.rect.collidepoint(mouse_pos):
                if not self.adding_edge_first_v:
                    self.adding_edge_first_v = v
                    return False
                else:
                    a, b = self.adding_edge_first_v.number, v.number
                    self.adj_list_undirected[a].append(b)
                    self.adj_list_undirected[b].append(a)
                    self.adj_list_directed[a].append(b)

                    if self.adding_edge_first_v.number == v.number:
                        self.edge_arr.append(Loop(v))
                    else:
                        self.add_edge(self.adding_edge_first_v, v)
                    if self.directing:
                        self.edge_arr[len(self.edge_arr) - 1].directing = True
                    self.adding_edge_first_v = None
                    return True
        return False

    def add_vertex(self, num: int, pos: Tuple[int, int]):
        self.vertex_dict[num] = Vertex(num, pos)

    def add_edge(self, a: Vertex, b: Vertex):
        self.edge_arr.append(Edge(a, b))

    def load_graph_from_file(self, file_path: str):
        self.__init__()
        try:
            with open(file_path, 'r') as file:
                try:
                    n, m = file.readline().split()
                    for i in range(int(n)):
                        self.adj_list_undirected[i+1] = []
                        self.adj_list_directed[i+1] = []
                    for i in range(int(m)):
                        a, b = file.readline().split()
                        a, b = int(a), int(b)

                        self.adj_list_undirected[a].append(b)
                        self.adj_list_undirected[b].append(a)

                        self.adj_list_directed[a].append(b)

                except ValueError:
                    print("Invalid file format")
                    return
        except FileNotFoundError:
            print("No file selected")
            return
        except TypeError:
            print("No file selected")
            return
        self.make_vertex_arr_from_adj_list()
        self.make_edge_arr_from_adj_list()

    def make_vertex_arr_from_adj_list(self):
        for v in self.adj_list_directed.keys():
            loop = True
            attempts = 0
            x, y = 0, 0
            while loop and attempts < 100:
                loop = False
                x = random.randint(Vertex.RADIUS, WIDTH - Vertex.RADIUS)
                y = random.randint(HEIGHT // 6 + Vertex.RADIUS, HEIGHT - Vertex.RADIUS)
                test_rect = pygame.Rect(x - Vertex.RADIUS, y - Vertex.RADIUS, 2*Vertex.RADIUS, 2*Vertex.RADIUS)
                for vertex in self.vertex_dict.values():
                    if test_rect.colliderect(vertex.rect):
                        loop = True
                        attempts += 1

            self.add_vertex(v, (x, y))

    def make_edge_arr_from_adj_list(self):
        for v1, v_list in self.adj_list_directed.items():
            for v2 in v_list:
                if v1 == v2:
                    self.edge_arr.append(Loop(self.vertex_dict[v1]))
                else:
                    self.add_edge(self.vertex_dict[v1], self.vertex_dict[v2])

