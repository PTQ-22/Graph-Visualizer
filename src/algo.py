import random
from collections import defaultdict, deque

import pygame

from src.constants import Colors
from src.graph import Graph


class AlgoController:

    def __init__(self, graph: Graph):
        self.visited = defaultdict()
        self.vis_queue = []
        self.graph = graph

    def clear_after_vis(self, time: int = 1200):
        pygame.time.wait(time)
        for v in self.graph.vertex_dict.values():
            v.color = Colors.GREY

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
            self.graph.draw(win)
            pygame.display.update()
            pygame.time.wait(400)
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
        print(self.graph.current_adj_list)
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

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def draw_mst_vis(self, win: pygame.Surface):
        pass
