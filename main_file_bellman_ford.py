"""
Here I included the code for
bellman-ford working case,
bellman-ford negative weight cycle detection
dijkstra's inf loop case

"""


from typing import final
import heapq
import math


class Edge:
    """Class that represents a basic edge"""
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
    @final
    def edge_id(src_v, dst_v):
        return (src_v.id, dst_v.id)

    def is_usable(self):
        return True


class Vertex:
    """Class that represents a basic vertex"""

    EdgeClass = Edge

    class Path:
        def __init__(self):
            self.reset()

        def reset(self):
            self.weight = math.inf
            self.from_vertex = None

        def __str__(self):
            return f"{self.__class__.__name__}=({self.weight}," \
                   f" {self.from_vertex.id if self.from_vertex else '(None)'})"

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
        return f"{self.__class__.__name__}=({self.id}, {self.out_edges}," \
               f" {self.path})"

    def __repr__(self):
        return str(self)


class Graph:
    """Class that represents a graph."""

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

    def __str__(self):
        vs = "\n".join([str(v) for v in self.vertices.values()])
        es = "\n".join([str(e) for e in self.edges.values()])
        return f"id={self.id}\n" \
               f"vertices:\n{vs}\n" \
               f"edges:\n{es}"

    def spf(self, src, dst):
        return self.dijkstra(src, dst)

    def dijkstra(self, src, dst):
        src_v = self.vertices[src]
        dst_v = self.vertices[dst]
        self._reset_paths()
        src_v.path.weight = 0
        src_v.path.from_vertex = src_v
        partial_paths = [src_v]

        while len(partial_paths):
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




if __name__ == "__main__":





    g3 = Graph("Dikstra's Limitation", vertices=['A', 'B', 'C', 'D', 'E', 'F'], edges=[('A', 'B', 5),
                                                       ('A', 'C', 35),
                                                       ('A', 'D', 40),
                                                       ('B', 'E', 25),
                                                       ('B', 'D', 20),
                                                       ('C', 'E', 30),
                                                       ('C', 'F', 30),
                                                       ('D', 'F', 20),
                                                       ('E', 'D', 45),
                                                       ('E', 'F', 25)])
    path, weight = g3.bellman_ford('A', 'F')
    #print(path, weight)

    g3_negative_edge = Graph("Dikstra's Limitation", vertices=['A', 'B', 'C', 'D', 'E', 'F'], edges=[('A', 'B', 5),
                                                       ('A', 'C', 35),
                                                       ('A', 'D', 40),
                                                       ('B', 'E', 25),
                                                       ('B', 'D', 20),
                                                       ('C', 'E', -30),
                                                       ('C', 'F', 30),
                                                       ('D', 'F', 20),
                                                       ('E', 'D', 45),
                                                       ('E', 'F', 25)])
    path, weight = g3_negative_edge.bellman_ford('A', 'F')
    #print(path, weight)


######### DETECTION OF NEGATIVE WEIGHT CYCLE
# This is the graph with negative weight cycle I used on my presentation
# Trying to go from V 1 to V 3
    g2 = Graph('Graph With Negative Weight Cycle', vertices=['1', '2', '3', '4'], edges=[('1', '2', 40),
                                                       ('1', '4', 50),
                                                       ('2', '4', 50),
                                                       ('4', '3', 30),
                                                       ('3', '2', -100)])

    #path, weight = g2.bellman_ford('1', '3')
    #print("Bellman-Ford:", path, weight)

##### DIJKSTRA's INF LOOP

# Same graph with negative weight cycle.
    path, weight = g2.dijkstra('1', '3')
    print("Dikstra's Inf Loop:", path, weight)





"""
g = Graph('G1', vertices=['A', 'B', 'C', 'D'], edges=[('A', 'B', 1), ('B', 'C', -3), ('A', 'C', 10), ('C', 'D', 3)])
path, weight = g.bellman_ford('B', 'D')
path1, weight1 = g.dijkstra('B', 'D')
print("Bellman-Ford Path:", path)
print("Bellman-Ford Weight:", weight)

print("Dijkstra Path:", path1)
print("Dijkstra Weight:", weight1)
"""







'''

g3_negative_edge2 = Graph("Dikstra's Limitation", vertices=['A', 'B', 'C', 'D', 'E', 'F', 'G'], edges=[('A', 'B', 4),
                                                       ('A', 'C', 2),
                                                       ('B', 'C', 5),
                                                       ('B', 'D', 10),
                                                       ('C', 'E', 3),
                                                       ('E', 'D', 4),
                                                        ('D', 'F', 11),
                                                       ('E', 'F', -10),
                                                       ('F', 'B', 10),
                                                        ('C', 'B', 15),
                                                                                                       ])

#path, weight = g3_negative_edge2.dijkstra('A', 'B')
#print(path, weight)

'''