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
        self.rect = pygame.Rect(pos[0] - self.RADIUS * Graph.scale, pos[1] - self.RADIUS * Graph.scale,
                                2*self.RADIUS * Graph.scale, 2*self.RADIUS * Graph.scale)
        self.color = Colors.GREY
        self.border_color = Colors.BLACK
        font = pygame.font.Font('freesansbold.ttf', int(40 * Graph.scale))
        self.text = font.render(str(self.number), True, Colors.BLACK)
        self.is_clicked = False

    def draw(self, win: pygame.Surface):
        self.rect.update(self.rect[0], self.rect[1], 2*self.RADIUS * Graph.scale, 2*self.RADIUS * Graph.scale)
        pygame.draw.circle(win, self.color, self.rect.center, self.RADIUS * Graph.scale)
        if self.is_clicked:
            pygame.draw.circle(win, Colors.GREEN, self.rect.center, self.RADIUS * Graph.scale,
                               int(self.LINE_SIZE * Graph.scale))
        else:
            pygame.draw.circle(win, self.border_color, self.rect.center, self.RADIUS * Graph.scale,
                               int(self.LINE_SIZE * Graph.scale))
        font = pygame.font.Font('freesansbold.ttf', int(40 * Graph.scale))
        self.text = font.render(str(self.number), True, Colors.BLACK)
        win.blit(self.text, self.text.get_rect(center=self.rect.center))

    def get_pos(self):
        return self.rect.center


class Edge:

    SIZE = 5

    def __init__(self, a: Vertex = None, b: Vertex = None, weight: int = 1):
        self.weight = weight
        self.color = Colors.BLACK
        self.directing = False
        self.weighted = False
        self.start = a
        self.end = b
        font = pygame.font.Font('freesansbold.ttf', int(25 * Graph.scale))
        self.text = font.render(str(self.weight), True, Colors.BLACK)

    def draw(self, win: pygame.Surface):
        if self.start and self.end:
            p1 = self.end.get_pos()
            p2 = self.start.get_pos()
            pygame.draw.line(win, self.color, p1, p2, int(self.SIZE * Graph.scale))
            if self.weighted:
                center = ((p1[0] + p2[0]) // 2 - int(5 * Graph.scale), (p1[1] + p2[1]) // 2 - int(15 * Graph.scale))
                font = pygame.font.Font('freesansbold.ttf', int(25 * Graph.scale))
                self.text = font.render(str(self.weight), True, Colors.BLACK)
                win.blit(self.text, self.text.get_rect(center=center))
            if self.directing:
                dist = int(50 * Graph.scale)

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

        p0 = rotate((0 + x, int(-10*Graph.scale) + y), angle)
        p1 = rotate((0 + x, int(10*Graph.scale) + y), angle)
        p2 = rotate((int(-20 * Graph.scale) + x, 0 + y), angle)

        pygame.draw.line(win, color, p0, p2, int(self.SIZE * Graph.scale))
        pygame.draw.line(win, color, p1, p2, int(self.SIZE * Graph.scale))


class Loop(Edge):

    def __init__(self, a: Vertex, weight: int = 1):
        super().__init__(a, a, weight)

    def draw(self, win: pygame.Surface):
        p = self.start.get_pos()
        pygame.draw.circle(win, self.color, (p[0] + int((Vertex.RADIUS + 5) * Graph.scale),
                                             p[1] - int((Vertex.RADIUS - 5) * Graph.scale)), int(20 * Graph.scale),
                           int(self.SIZE * Graph.scale))
        if self.weighted:
            center = (p[0] + int((Vertex.RADIUS + 5) * Graph.scale), p[1] - int((Vertex.RADIUS + 25) * Graph.scale))
            win.blit(self.text, self.text.get_rect(center=center))
        if self.directing:
            self.draw_arrow(win, p[0] + int((Vertex.RADIUS + 10) * Graph.scale), p[1] - int(15 * Graph.scale),
                            self.color, 40)


class Graph:

    scale = 1

    def __init__(self):
        self.adj_list_undirected = defaultdict(list)
        self.adj_list_directed = defaultdict(list)
        self.current_adj_list = self.adj_list_undirected
        self.vertex_dict: defaultdict[int, Vertex] = defaultdict()
        self.edge_arr: List[Edge] = []

        self.adding_edge = False
        self.adding_edge_first_v = None
        self.directing = False
        self.weighted = False

    def draw(self, win: pygame.Surface):
        for e in self.edge_arr:
            e.draw(win)
        if self.adding_edge:
            pos = pygame.mouse.get_pos()
            if self.adding_edge_first_v:
                pygame.draw.line(win, Colors.BLACK, pos, self.adding_edge_first_v.get_pos(),
                                 int(Edge.SIZE * Graph.scale))
            else:
                pygame.draw.line(win, Colors.BLACK, pos, (pos[0]+10, pos[1]+5), int(Edge.SIZE * Graph.scale))
        for v in self.vertex_dict.values():
            v.draw(win)

    def update(self):
        """
        updates nodes position if they are moved by mouse
        """
        for v in self.vertex_dict.values():
            if v.is_clicked:
                v.rect.center = pygame.mouse.get_pos()

    def change_directing(self, d: bool):
        """
        update edges and current adjacency list
        """
        if self.current_adj_list is self.adj_list_directed:
            self.current_adj_list = self.adj_list_undirected
        else:
            self.current_adj_list = self.adj_list_directed
        for e in self.edge_arr:
            e.directing = d
        self.directing = d

    def change_weighted(self, w: bool):
        for e in self.edge_arr:
            e.weighted = w
        self.weighted = w

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
                    if b not in self.adj_list_directed.keys():
                        self.adj_list_directed[b] = []

                    if self.adding_edge_first_v.number == v.number:
                        self.edge_arr.append(Loop(v))
                    else:
                        self.add_edge(self.adding_edge_first_v, v, 1)
                    if self.directing:
                        self.edge_arr[len(self.edge_arr) - 1].directing = True
                    if self.weighted:
                        self.edge_arr[len(self.edge_arr) - 1].weighted = True
                    self.adding_edge_first_v = None
                    return True
        return False

    def add_vertex(self, num: int, pos: Tuple[int, int]):
        self.vertex_dict[num] = Vertex(num, pos)

    def add_edge(self, a: Vertex, b: Vertex, w: int):
        self.edge_arr.append(Edge(a, b, w))

    def load_graph_from_file(self, file_path: str):
        self.__init__()
        weights = defaultdict()
        try:
            with open(file_path, 'r') as file:
                try:
                    n, m = file.readline().split()
                    for i in range(int(n)):
                        self.adj_list_undirected[i+1] = []
                        self.adj_list_directed[i+1] = []
                    for i in range(int(m)):
                        values = file.readline().split()
                        if len(values) == 3:
                            a, b, c = values
                            weights[f'{a}-{b}'] = c
                        else:
                            a, b = values
                            weights[f'{a}-{b}'] = 1
                        a, b = int(a), int(b)

                        self.adj_list_undirected[a].append(b)
                        self.adj_list_undirected[b].append(a)

                        self.adj_list_directed[a].append(b)

                except ValueError as e:
                    print(e)
                    print("Invalid file format")
                    return
        except FileNotFoundError:
            print("No file selected")
            return
        except TypeError:
            print("No file selected")
            return
        self.make_vertex_arr_from_adj_list()
        self.make_edge_arr_from_adj_list(weights)

    def make_vertex_arr_from_adj_list(self):
        for v in self.adj_list_directed.keys():
            loop = True
            attempts = 0
            x, y = 0, 0
            while loop and attempts < 100:
                loop = False
                x = random.randint(int(Vertex.RADIUS * Graph.scale), WIDTH - int(Vertex.RADIUS * Graph.scale))
                y = random.randint(HEIGHT // 5 + int(Vertex.RADIUS * Graph.scale),
                                   HEIGHT - int(Vertex.RADIUS * Graph.scale))
                test_rect = pygame.Rect(x - int(Vertex.RADIUS * Graph.scale), y - int(Vertex.RADIUS * Graph.scale),
                                        2*int(Vertex.RADIUS * Graph.scale), 2*int(Vertex.RADIUS * Graph.scale))
                for vertex in self.vertex_dict.values():
                    if test_rect.colliderect(vertex.rect):
                        loop = True
                        attempts += 1

            self.add_vertex(v, (x, y))

    def make_edge_arr_from_adj_list(self, weights: defaultdict):
        for v1, v_list in self.adj_list_directed.items():
            for v2 in v_list:
                if v1 == v2:
                    self.edge_arr.append(Loop(self.vertex_dict[v1], weights[f'{v1}-{v2}']))
                else:
                    self.add_edge(self.vertex_dict[v1], self.vertex_dict[v2], weights[f'{v1}-{v2}'])

