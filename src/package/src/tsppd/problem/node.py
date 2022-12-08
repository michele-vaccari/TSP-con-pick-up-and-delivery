import math

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

    @property
    def id(self):
        return self._id
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @classmethod
    def from_json(self, json_node):
        return Node(int(json_node["id"]), int(json_node["x"]), int(json_node["y"]))
    
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
        return "node[{}] = ({}, {})".format(self._id, self._x, self._y)