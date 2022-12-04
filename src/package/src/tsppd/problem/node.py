class Node:

    def __init__(self, name: str, x: float, y: float):
        """
        Create node for TSPPD problem.
        :param name: node name
        :param x: node abscissa
        :param y: node ordinate
        """
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.name) + " x = {} y = {}".format(self.x, self.y)