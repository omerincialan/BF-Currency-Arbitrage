# This part is to measure and understand the time complexity
# of Bellman-Ford's algorithm

import time
import heapq
import math
import random

class Edge:
    def __init__(self, id_, src, dst, weight=1):
        self.id = id_
        self.src = src
        self.dst = dst
        self.weight = weight

    def __str__(self):
        return f"{self.__class__.__name__}=({self.id}: {self.weight})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def edge_id(src_v, dst_v):
        return (src_v.id, dst_v.id)

    def is_usable(self):
        return True

class Vertex:
    EdgeClass = Edge

    class Path:
        def __init__(self):
            self.reset()

        def reset(self):
            self.weight = math.inf
            self.from_vertex = None

        def __str__(self):
            return f"{self.__class__.__name__}=({self.weight}, {self.from_vertex.id if self.from_vertex else '(None)'})"

    def __init__(self, id_):
        self.id = id_
        self.out_edges = set()
        self.path = Vertex.Path()

    def add_edge(self, id_, dst, weight=1):
        edge = self.EdgeClass(id_, self, dst, weight)
        self.out_edges.add(edge)
        return edge

    def __lt__(self, other):
        return self.path.weight < other.path.weight

    def __str__(self):
        return f"{self.__class__.__name__}=({self.id}, {self.out_edges}, {self.path})"

    def __repr__(self):
        return str(self)

class Graph:
    VertexClass = Vertex

    def __init__(self, id_, vertices=None, edges=None):
        self.id = id_
        self.vertices = dict()
        self.edges = dict()

        if vertices is not None:
            for vertex in vertices:
                self.add_vertex(vertex)

        if edges is not None:
            for edge in edges:
                self.add_edge(*edge)

    def add_vertex(self, id_):
        v = self.VertexClass(id_)
        self.vertices[id_] = v

    def add_edge(self, src, dst, weight=1):
        src_v = self.vertices[src]
        dst_v = self.vertices[dst]
        edge_id = Edge.edge_id(src_v, dst_v)
        edge = src_v.add_edge(edge_id, dst_v, weight)
        self.edges[edge_id] = edge

    def dijkstra(self, src, dst):
        src_v = self.vertices[src]
        dst_v = self.vertices[dst]
        self._reset_paths()
        src_v.path.weight = 0
        src_v.path.from_vertex = src_v
        partial_paths = [src_v]

        while partial_paths:
            min_vertex = heapq.heappop(partial_paths)

            for edge in min_vertex.out_edges:
                if not edge.is_usable():
                    continue
                dest_vertex = edge.dst
                new_weight = min_vertex.path.weight + edge.weight

                if new_weight < dest_vertex.path.weight:
                    dest_vertex.path.weight = new_weight
                    dest_vertex.path.from_vertex = min_vertex

                    if dest_vertex in partial_paths:
                        heapq.heapify(partial_paths)
                    else:
                        heapq.heappush(partial_paths, dest_vertex)

        return self._build_spf(src_v, dst_v)

    def bellman_ford(self, src, dst):
        src_v = self.vertices[src]
        dst_v = self.vertices[dst]
        self._reset_paths()
        src_v.path.weight = 0

        for _ in range(len(self.vertices) - 1):
            for edge in self.edges.values():
                if not edge.is_usable():
                    continue
                src_vertex = self.vertices[edge.src.id]
                dst_vertex = self.vertices[edge.dst.id]
                new_weight = src_vertex.path.weight + edge.weight

                if new_weight < dst_vertex.path.weight:
                    dst_vertex.path.weight = new_weight
                    dst_vertex.path.from_vertex = src_vertex

        for edge in self.edges.values():
            src_vertex = self.vertices[edge.src.id]
            dst_vertex = self.vertices[edge.dst.id]
            if src_vertex.path.weight + edge.weight < dst_vertex.path.weight:
                raise ValueError("Graph contains a negative-weight cycle")

        return self._build_spf(src_v, dst_v)

    def _reset_paths(self):
        for v in self.vertices.values():
            v.path.reset()

    def _build_spf(self, src_v, dst_v):
        v = dst_v
        path = [v]
        while v is not src_v and v.path.from_vertex is not None:
            path.insert(0, v.path.from_vertex)
            v = v.path.from_vertex

        return [v.id for v in path], dst_v.path.weight

def generate_random_graph(num_vertices, num_edges):
    vertices = [str(i) for i in range(num_vertices)]
    edges = []

    for _ in range(num_edges):
        src = random.choice(vertices)
        dst = random.choice(vertices)
        while dst == src:
            dst = random.choice(vertices)
        weight = random.uniform(-1, 10)
        edges.append((src, dst, weight))

    return vertices, edges

def measure_time_performance(num_vertices, num_edges, src, dst):
    vertices, edges = generate_random_graph(num_vertices, num_edges)
    graph = Graph('G1', vertices=vertices, edges=edges)

    # Measure Dijkstra's algorithm time
    start_time = time.time()
    try:
        graph.dijkstra(src, dst)
    except KeyError:
        pass
    dijkstra_time = time.time() - start_time

    # Measure Bellman-Ford algorithm time
    start_time = time.time()
    try:
        graph.bellman_ford(src, dst)
    except ValueError:
        pass
    except KeyError:
        pass
    bellman_ford_time = time.time() - start_time

    print(f"Dijkstra's algorithm time: {dijkstra_time:.6f} seconds")
    print(f"Bellman-Ford algorithm time: {bellman_ford_time:.6f} seconds")


num_vertices = 3500
num_edges = 3500
src = '0'
dst = '99'
measure_time_performance(num_vertices, num_edges, src, dst)
