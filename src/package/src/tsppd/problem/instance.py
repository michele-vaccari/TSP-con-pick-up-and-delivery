import json

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
    
    
    def save_to_json(self, path: str):
        with open(path, "w", encoding="utf-8") as output:
            json.dump(self._to_json(), output, ensure_ascii=False, indent=4)

    #def read_from_file(self, path: str):

    def _to_json(self):
        json_nodes = []
        for node in self.nodes:
            json_nodes.append(node.to_json())
        
        json_weighted_edges = []
        for weighted_edge in self.weighted_edges:
            json_weighted_edges.append(weighted_edge.to_json())
        
        json_requests = []
        for request in self.requests:
            json_requests.append(request.to_json())

        return {
            "nodes": json_nodes,
            "weighted_edges": json_weighted_edges,
            "requests": json_requests
        }

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