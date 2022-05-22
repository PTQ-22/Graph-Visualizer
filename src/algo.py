import random
from queue import PriorityQueue
from collections import defaultdict, deque
from typing import List

import pygame

from src.constants import Colors, INFINITY
from src.graph import Graph, Edge


class AlgoController:

    def __init__(self, graph: Graph):
        self.visited = defaultdict()
        self.vis_queue = []
        self.graph = graph

    def clear_after_vis(self, time: int = 1200):
        pygame.time.wait(time)
        for v in self.graph.vertex_dict.values():
            v.color = Colors.GREY
            v.border_color = Colors.BLACK
        for e in self.graph.edge_arr:
            e.color = Colors.BLACK

    def redraw_window(self, win: pygame.Surface):
        self.graph.draw(win)
        pygame.display.update()
        pygame.time.wait(400)


class DfsVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def draw_dfs_vis(self, win: pygame.Surface):
        print(self.graph.current_adj_list)
        for v in self.graph.current_adj_list.keys():
            self.visited[v] = False

        self.dfs(1)

        for v, order in self.vis_queue:
            if order == 'in':
                self.graph.vertex_dict[v].color = Colors.YELLOW
            elif order == 'out':
                self.graph.vertex_dict[v].color = Colors.GREEN
            self.redraw_window(win)
        self.clear_after_vis()

    def dfs(self, v: int):
        self.visited[v] = True
        self.vis_queue.append((v, 'in'))
        for u in self.graph.current_adj_list[v]:
            if not self.visited[u]:
                self.dfs(u)
        self.vis_queue.append((v, 'out'))


class BfsVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.dist = defaultdict()

    def draw_bfs_vis(self, win: pygame.Surface):
        for v in self.graph.current_adj_list.keys():
            self.visited[v] = False
            self.dist[v] = -1

        self.bfs(1)
        color = (0, 255, 0)
        color_change = 70
        current_p = 0
        for v, phase in self.vis_queue:
            if phase != current_p:
                current_p = phase
                color = (0, color[1] - color_change, 0)
                if color[1] < 0:
                    color = (0, 255, 0)
            self.graph.vertex_dict[v].color = color
            self.redraw_window(win)
        self.clear_after_vis()

    def bfs(self, v: int):
        q = deque([v])
        self.visited[v] = True
        self.dist[v] = 0
        while len(q) > 0:
            v = q.popleft()
            self.vis_queue.append((v, self.dist[v]))
            for u in self.graph.current_adj_list[v]:
                if not self.visited[u]:
                    q.append(u)
                    self.dist[u] = self.dist[v] + 1
                    self.visited[u] = True


class SCCvis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.scc_num = defaultdict()
        self.postorder = []
        self.transp_graph_adj = defaultdict(list)

    def draw_scc_vis(self, win: pygame.Surface):
        for v in self.graph.adj_list_directed.keys():
            self.visited[v] = False
            self.scc_num[v] = 0

        n = self.scc()
        colors = []
        for i in range(n):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            while color in colors:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colors.append(color)
        for v, scc_n in self.scc_num.items():
            self.graph.vertex_dict[v].color = colors[scc_n - 1]
        self.redraw_window(win)
        self.clear_after_vis(3000)

    def scc(self) -> int:
        for i in self.graph.adj_list_directed.keys():
            if not self.visited[i]:
                self.postorder_dfs(i)
        self.postorder.reverse()
        self.build_transp_graph()
        scc_counter = 1
        for p in self.postorder:
            if self.scc_num[p] == 0:
                self.dfs_transp(p, scc_counter)
                scc_counter += 1
        return scc_counter - 1

    def postorder_dfs(self, v: int):
        self.visited[v] = True
        for u in self.graph.adj_list_directed[v]:
            if not self.visited[u]:
                self.postorder_dfs(u)
        self.postorder.append(v)

    def build_transp_graph(self):
        for a in self.graph.adj_list_directed.keys():
            for b in self.graph.adj_list_directed[a]:
                self.transp_graph_adj[b].append(a)

    def dfs_transp(self, v: int, scc_counter: int):
        self.scc_num[v] = scc_counter
        for u in self.transp_graph_adj[v]:
            if self.scc_num[u] == 0:
                self.dfs_transp(u, scc_counter)


class MSTvis(AlgoController):

    class DSU:
        def __init__(self, nodes: List[int]):
            self.rep = defaultdict()
            self.set_size = defaultdict()
            for v in nodes:
                self.rep[v] = v
                self.set_size[v] = 1

        def find(self, a: int):
            if self.rep[a] == a:
                return a
            self.rep[a] = self.find(self.rep[a])
            return self.rep[a]

        def join(self, a: int, b: int):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.set_size[a] > self.set_size[b]:
                a, b = b, a
            self.set_size[b] += self.set_size[a]
            self.rep[a] = b

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.dsu = self.DSU(graph.current_adj_list.keys())
        self.edges: List[Edge] = []
        self.mst: List[Edge] = []

    def draw_mst_vis(self, win: pygame.Surface):
        self.find_mst()
        for e in self.mst:
            e.color = Colors.CYAN
        for v in self.graph.vertex_dict.values():
            v.border_color = Colors.CYAN

        self.redraw_window(win)
        self.clear_after_vis(3000)

    def find_mst(self):
        for e in self.graph.edge_arr:
            self.edges.append(e)
        self.edges.sort(key=lambda edge: int(edge.weight))

        for e in self.edges:
            if self.dsu.find(e.start.number) != self.dsu.find(e.end.number):
                self.dsu.join(e.start.number, e.end.number)
                self.mst.append(e)


class DijkstraVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.dist = defaultdict()
        self.weighted_graph = defaultdict(list)

    def draw_dijkstra_vis(self, win: pygame.Surface):
        for v in self.graph.current_adj_list.keys():
            self.visited[v] = False
            self.dist[v] = INFINITY
        self.make_weighted_graph_rep()

        self.dijkstra(1)

        for v in self.vis_queue:
            self.graph.vertex_dict[v].color = Colors.YELLOW
            self.redraw_window(win)
        self.clear_after_vis()

    def dijkstra(self, start: int):
        pq = PriorityQueue()
        pq.put((0, start))
        self.dist[start] = 0

        while not pq.empty():
            v = pq.get()[1]
            if self.visited[v]:
                continue
            self.visited[v] = True
            self.vis_queue.append(v)
            for p in self.weighted_graph[v]:
                u, w = p
                if self.dist[v] + w < self.dist[u]:
                    self.dist[u] = self.dist[v] + w
                    pq.put((-w, u))

    def make_weighted_graph_rep(self):
        for e in self.graph.edge_arr:
            a = int(e.start.number)
            b = int(e.end.number)
            w = int(e.weight)
            if self.graph.directing:
                self.weighted_graph[a].append((b, w))
            else:
                self.weighted_graph[a].append((b, w))
                self.weighted_graph[b].append((a, w))


class BridesAndArticPointsVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.pre = defaultdict()
        self.low = defaultdict()
        self.is_art_point = defaultdict()
        for v in self.graph.current_adj_list.keys():
            self.pre[v] = 0
            self.low[v] = 0
            self.is_art_point[v] = False
        self.pre_counter = 0

    def draw_bridges_vis(self, win: pygame.Surface):
        self.dfs(1, -1)

        for e in self.graph.edge_arr:
            a = e.start.number
            b = e.end.number
            if self.pre[a] > self.pre[b]:
                a, b = b, a
            if self.low[b] > self.pre[a]:
                e.color = Colors.RED
        self.redraw_window(win)
        self.clear_after_vis(3000)

    def draw_artic_points_vis(self, win: pygame.Surface):
        self.dfs(1, -1)

        for v in self.graph.vertex_dict.values():
            if self.is_art_point[v.number]:
                v.color = Colors.RED

        self.redraw_window(win)
        self.clear_after_vis(3000)

    def dfs(self, v: int, pred: int):
        if self.low[v] != 0:
            return self.pre[v]
        self.pre_counter += 1
        self.pre[v] = self.low[v] = self.pre_counter
        c = 0
        for u in self.graph.adj_list_undirected[v]:
            if u != pred:
                c += 1
                self.low[v] = min(self.low[v], self.dfs(u, v))
                if pred != -1 and self.low[u] >= self.pre[v]:
                    self.is_art_point[v] = True

        if pred == -1 and c > 1:
            self.is_art_point[v] = True

        return self.low[v]
