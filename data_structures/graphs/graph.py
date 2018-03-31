import abc
import collections
import functools
import math
from .error import GraphError
from .info import Vertex, UndirectedEdge
from queues import PriorityQueue



class _BaseGraph(metaclass=abc.ABCMeta):
    def __init__(self):
        """
        _adjacency_map: {T: Vertex}
        """
        self._adjacency_map = {}
        self._root = None
        self.__edge_type = None
        self.__vertex_type = None


    @property
    @abc.abstractmethod
    def _EdgeType(self) -> type:
        """
        Base class methods common to all graphs will use the type returned by this property
        to add edges between vertices.

        e.g., _EdgeType will return UndirectedEdge in an UndirectedGraph
        """
        pass


    @_EdgeType.setter
    def _EdgeType(self, new_edge_type: type) -> None:
        self.__edge_type = new_edge_type


    @property
    @abc.abstractmethod
    def _VertexType(self) -> type:
        pass


    @_VertexType.setter
    def _VertexType(self, new_vertex_type: type) -> None:
        self.__vertex_type = new_vertex_type


    def __len__(self) -> int:
        return len(self._adjacency_map)


    def __bool__(self) -> bool:
        return len(self) > 0


    def __contains__(self, vertex_value) -> bool:
        return vertex_value in self._adjacency_map


    def __getitem__(self, vertex_value) -> Vertex:
        if vertex_value not in self:
            raise GraphError('vertex with value {0} does not exist'.format(vertex_value))
        return self._adjacency_map[vertex_value]


    def vertices(self) -> [Vertex]:
        return list(self._adjacency_map.values())


    @abc.abstractmethod
    def edges(self) -> ['_BaseEdge']:
        pass


    def add_vertex(self, new_vertex_value, dst_vertex_value=None, weight=0) -> None:
        """
        Adds a vertex from the origin vertex to the destination vertex.
        If dst_vertex_value is None, a lone vertex is added, disconnecting the graph.
        Otherwise, specifying a dst_vertex_value will connect an edge between the 2 argument vertices.
        """
        origin = self[new_vertex_value] if new_vertex_value in self else self._VertexType(new_vertex_value)
        if not self:
            self._root = origin

        self._adjacency_map[new_vertex_value] = origin
        if dst_vertex_value is not None:
            self._adjacency_map[dst_vertex_value] = self._VertexType(dst_vertex_value)
            self.add_edge(new_vertex_value, dst_vertex_value, weight=weight)


    @abc.abstractmethod
    def add_edge(self, origin_vertex_value, dst_vertex_value, weight=0) -> None:
        pass


    def dijkstra(self, origin_vertex_value, destination_vertex_value) -> collections.deque([Vertex]):
        labels = {}
        parents = {}
        for v in self.vertices():
            labels[v] = math.inf
            parents[v] = None
        labels[self[origin_vertex_value]] = 0
        table = PriorityQueue([v for v in self.vertices()], key=lambda v: labels[v], reverse=True)  # min-heap

        while table:
            start = table.pop()
            for adjacent_edge in start.outgoing_edges:
                end = adjacent_edge.destination
                index = table.find(end)
                if index != -1:
                    weighted_distance = labels[start] + adjacent_edge.weight
                    if weighted_distance < labels[end]:
                        labels[end] = weighted_distance
                        table.remove(index)
                        table.push(end)
                        parents[end] = start

        result = collections.deque()
        start = self[destination_vertex_value]
        while start is not None:
            result.appendleft(start)
            start = parents[start]
        return result


    def bellman_ford(self, origin_vertex_value, destination_vertex_value) -> collections.deque([Vertex]):
        labels = {}
        parents = {}
        for v in self.vertices():
            labels[v] = math.inf
            parents[v] = None
        labels[self[origin_vertex_value]] = 0
        i = 0
        stop_limit = len(self) - 1

        while i < stop_limit:
            for edge in self.edges():
                start = edge.origin
                end = edge.destination
                weighted_distance = labels[start] + edge.weight
                if weighted_distance < labels[end]:
                    labels[end] = weighted_distance
                    parents[end] = start
            i += 1

        if all(labels[e.destination] <= labels[e.origin] + e.weight for e in self.edges()):
            result = collections.deque()
            start = self[destination_vertex_value]
            while start is not None:
                result.appendleft(start)
                start = parents[start]
            return result
        else:
            raise GraphError('negative-weight cycle')



class UndirectedGraph(_BaseGraph):
    """
    Implementation for an undirected, optionally-weighted graph.
    Utilizes a dictionary (hash map) for O(1) lookup/modification/removal operations,
    as opposed to a typical adjacency list, which is more space efficient but provides higher time complexity.
    """

    @property
    def _EdgeType(self) -> type:
        return UndirectedEdge

    @property
    def _VertexType(self) -> type:
        return Vertex
    
    def print(self):
        for item, vertex in self._adjacency_map.items():
            print('  {0}: {1}'.format(item, vertex.readable_string()))
            
            
    def has_edge(self, origin_vertex_value, dst_vertex_value, weight=0) -> bool:
        """
        Returns True if an edge exists between the origin vertex and destination vertex.
        In an undirected graph, edge containment is a symmetric property - 
        if an edge exists between the origin and destination vertices, 
        then it also exists between the destination and origin vertices.
        As an optimization, only the "outgoing" edge (origin -> destination) is verified - 
        but for unit testing, both should be verified.
        
        Raises GraphError if either vertex does not exist.
        """
        origin = self[origin_vertex_value]
        destination = self[dst_vertex_value]
        outgoing = self._EdgeType(origin, destination, weight=weight)
        
        return outgoing in origin.edges
    
    
    def edge_count(self, unique=True) -> int:
        """
        Returns the total number of edges in the graph.
        Set unique=True to count unique edges only.
        """
        if unique:
            result = set()
            for vertex in self._adjacency_map.values():
                result.update(vertex.edges)
            return len(result)

        else:
            return sum((len(v.edges) for v in self._adjacency_map.values()))


    def edges(self) -> {UndirectedEdge}:
        return functools.reduce(set.union, (v.outgoing_edges for v in sorted(self.vertices(), key=lambda x: x.value)), set())
            
            
    def add_edge(self, origin_vertex_value, dst_vertex_value, weight=0) -> None:
        """
        Adds an edge from the origin vertex to the destination vertex.
        Does nothing if an edge already exists.
        Raises GraphError if either vertex does not exist.
        """
        origin = self[origin_vertex_value]
        destination = self[dst_vertex_value]
        outgoing = self._EdgeType(origin, destination, weight=weight)
        incoming = self._EdgeType(destination, origin, weight=weight)

        origin.edges.add(outgoing)
        destination.edges.add(incoming)
        
        
    def is_complete(self) -> bool:
        """
        Returns True if this graph is complete.
        A complete graph is an undirected graph with an edge between every pair of vertices.
        A complete graph of 'n' vertices has m = C(n, 2) edges (n "choose" 2).
        An empty graph, or a graph with 1 vertex is considered incomplete.
        """
        pass


    def is_connected(self) -> bool:
        """
        Returns True if this graph is connected.
        An undirected graph is connected if there is a path between any pair of vertices.
        This is tested by performing a depth-first search.
        An empty graph is considered disconnected.
        A graph of 1 vertex is considered connected.
        """
        if not self:
            return False
        return self._dfs_is_connected(self._root, set()) == len(self)


    def is_reachable(self, origin_vertex_value, destination_vertex_value) -> bool:
        """
        Returns True if vertex destination is reachable from vertex origin.
        Destination is reachable from origin if a path exists between them.
        Performs a depth-first search starting at origin to test this.
        """
        root = self[origin_vertex_value]
        destination = self[destination_vertex_value]
        return self._dfs_is_reachable(root, destination, set())


    def _dfs_is_connected(self, root: Vertex, explored: {Vertex}) -> int:
        explored.add(root)
        for edge in root.edges:
            destination = edge.destination
            if destination not in explored:
                self._dfs_is_connected(destination, explored)
        return len(explored)


    def _dfs_is_reachable(self, root: Vertex, destination: Vertex, explored: {Vertex}) -> bool:
        if root == destination:
            return True
        explored.add(root)
        result = False
        for edge in root.edges:
            opposite = edge.destination
            if opposite not in explored:
                result = result or self._dfs_is_reachable(opposite, destination, explored)
                if result:
                    break

        return result



if __name__ == '__main__':
    pass