class Node:

    def __init__(self, id: int, x: float, y: float):
        """
        Create node for TSPPD problem.
        :param id: node id
        :param x: node abscissa
        :param y: node ordinate
        """
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "node -> id = {} x = {} y = {}".format(self.id, self.x, self.y)