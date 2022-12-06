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

    def __str__(self):
        return "node -> id = {} x = {} y = {}".format(self._id, self._x, self._y)