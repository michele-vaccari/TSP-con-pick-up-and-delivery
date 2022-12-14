import math
from .weightedEdge import WeightedEdge

class Node:

    def __init__(self, id: int, x: float, y: float):
        """
        Create node for TSPPD problem.
        :param id: node id
        :param x: node abscissa
        :param y: node ordinate
        """
        self._id = id
        self._x = x
        self._y = y
        self._weighted_edges = []

    @property
    def id(self):
        return self._id
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def weighted_edges(self):
        return self._weighted_edges
    
    @classmethod
    def from_json(self, json_node):
        return Node(int(json_node["id"]), int(json_node["x"]), int(json_node["y"]))
    
    def add_weighted_edge(self, weighted_edge: WeightedEdge):
        self._weighted_edges.append(weighted_edge)
    
    def sort_weighted_edges_by_ascending_weight(self):
        self._weighted_edges.sort()
    
    def to_json(self):
        return { "id": self.id, "x": self.x, "y": self.y }
    
    def euclidean_distance(self, other):
        if isinstance(other, Node):
            return round(math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2), 2)
        return NotImplemented

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.id == other.id and self.x == other.x and self.y == other.y
        return NotImplemented

    def __str__(self):
        output = "node[{}] = ({}, {})\n".format(self._id, self._x, self._y)
        output += "Weighted edge of node[{}]:\n".format(self._id)
        for weighted_edge in self.weighted_edges:
            output += "{}\n".format(str(weighted_edge))
        return output
        
