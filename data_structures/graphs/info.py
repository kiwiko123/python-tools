import abc


class Vertex:
    def __init__(self, value):
        self._value = value
        self._edges = set()
    
    def __repr__(self) -> str:
        return '{0}({1})'.format(type(self).__name__, self.value)
    
    
    def __bool__(self) -> bool:
        return bool(self.value)
    
    
    def __hash__(self) -> int:
        return hash('Vertex({0})'.format(repr(self.value)))
    
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Vertex) and self.value == other.value
    
    
    def readable_string(self) -> str:
        body = '\n  '.join([str(e) for e in self.edges])
        return '{0}({1}, {2})'.format(type(self).__name__, self.value, body)
    
        
    @property
    def value(self):
        return self._value
    
    
    @property
    def edges(self) -> {'Edge'}:
        return self._edges


    @property
    def outgoing_edges(self) -> {'Edge'}:
        return self.edges


    @property
    def incoming_edges(self) -> {'Edge'}:
        return self.edges


    def outdegree(self) -> int:
        return len(self.outgoing_edges)


    def indegree(self) -> int:
        return len(self.incoming_edges)
    
    
    def degree(self) -> int:
        return len(self.edges)
    
    
    def add_edge(self, destination: 'Vertex', weight=0) -> None:
        edge = UndirectedEdge(self, destination, weight=weight)
        self.edges.add(edge)
    
    

class DigraphVertex(Vertex):
    def __init__(self, value):
        self._outgoing_edges = set()
        self._incoming_edges = set()
        
    @property
    def outgoing_edges(self) -> set:
        return self._outgoing_edges
    
    @property
    def incoming_edges(self) -> set:
        return self._incoming_edges
    
    def degree(self) -> int:
        return self.outdegree() + self.indegree()



class _BaseEdge(metaclass=abc.ABCMeta):
    def __init__(self, origin: Vertex, destination: Vertex, weight=0):
        self._origin = origin
        self._destination = destination
        self._weight = weight
        
    def __repr__(self) -> str:
        return '{0}({1}, {2}, {3})'.format(type(self).__name__, repr(self.origin), repr(self.destination), repr(self.weight))
    
    def __hash__(self) -> int:
        return hash(repr(self))
    
    @abc.abstractmethod
    def __eq__(self, other) -> bool:
        pass
        
    @property
    def origin(self) -> Vertex:
        return self._origin
    
    @property
    def destination(self) -> Vertex:
        return self._destination
        
    @property
    def weight(self) -> int or float:
        return self._weight
    
    @weight.setter
    def weight(self, new_weight: int or float) -> None:
        self._weight = new_weight
    
    
    
class UndirectedEdge(_BaseEdge):
    def __str__(self) -> str:
        return '{0}({1} - {2})'.format(type(self).__name__, self.origin.value, self.destination.value)

    def __eq__(self, other) -> bool:
        return isinstance(other, UndirectedEdge) and \
               self.origin == other.destination and \
               self.destination == other.origin and \
               self.weight == other.weight
    
    def __hash__(self) -> int:
        """
        An undirected edge hashes equal to another undirected edge,
        if its origin and destination vertices are combinations of each other and their weights are equal.
        For example, hash(UndirectedEdge(1 -> 2)) == hash(UndirectedEdge(2 -> 1)). 
        """
        return hash(type(self).__name__) + hash(self.origin) + hash(self.destination) + hash(self.weight)


class DirectedEdge(_BaseEdge):
    def __str__(self) -> str:
        return '{0}({1} -> {2} (weight={3}))'.format(type(self).__name__, self.origin.value, self.destination.value, self.weight)

    def __eq__(self, other) -> bool:
        return isinstance(other, DirectedEdge) and \
               self.origin == other.destination and \
               self.destination == other.origin and \
               self.weight == other.weight

    def __hash__(self) -> int:
        """
        A directed edge e1 hashes equal to another directed edge e2,
        if its origin and destination vertices are equal (e1.origin == e2.origin and e1.destination == e2.destination),
        and weights are equal.
        """
        return hash(repr(self))