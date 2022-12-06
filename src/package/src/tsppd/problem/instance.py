class Instance:
    def __init__(self, nodes: list, requests: list):
        """
        Instance of TSPPD problem.
        :param nodes: list of problem nodes
        :param requests: list of problem requests
        """
        self._nodes = nodes
        self._requests = requests

    @property
    def nodes(self):
        return self._nodes

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
        output += "REQUESTS:\n"
        for request in self.requests:
            output += str(request) + "\n"
        return output