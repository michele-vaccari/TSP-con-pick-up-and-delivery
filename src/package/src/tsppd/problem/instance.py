class Instance:
    def __init__(self, nodes: list, weighted_edges: list, requests: list):
        """
        Instance of TSPPD problem.
        :param nodes: list of problem nodes
        :param weighted_edges: list of problem weighted edges
        :param requests: list of problem requests
        """
        self._nodes = nodes
        self._weighted_edges = weighted_edges
        self._requests = requests

    @property
    def nodes(self):
        return self._nodes

    @property
    def weighted_edges(self):
        return self._weighted_edges

    @property
    def requests(self):
        return self._requests
    
    #TODO
    #def write_to_file(self, path: str):
    #def read_from_file(self, path: str):

    def __str__(self):
        output = "NODES:\n"
        for node in self.nodes:
            output += str(node) + "\n"
        output += "WEIGHTED EDGES:\n"
        for weigted_edge in self.weighted_edges:
            output += str(weigted_edge) + "\n"
        output += "REQUESTS:\n"
        for request in self.requests:
            output += str(request) + "\n"
        return output