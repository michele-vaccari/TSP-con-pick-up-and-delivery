class WeightedEdge:
    def __init__(self, id_i_node: int, id_j_node: int, weight: float):
        """
        Create edge for TSPPD problem.
        :param id_i_node: i node id
        :param id_j_node: j node id
        :param weight: cost from node i to node j
        """
        self._id_i_node = id_i_node
        self._id_j_node = id_j_node
        self._weight = weight

    @property
    def id_i_node(self):
        return self._id_i_node

    @property
    def id_j_node(self):
        return self._id_j_node
    
    @property
    def weight(self):
        return self._weight

    def __str__(self):
        return "({}, {}, {})".format(self.id_i_node, self.id_j_node, self.weight)