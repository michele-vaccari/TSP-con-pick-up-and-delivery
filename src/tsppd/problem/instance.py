import json
from .node import Node
from .weightedEdge import WeightedEdge
from .request import Request
class Instance:
    def __init__(self, nodes: dict, weighted_edges: list, requests: list):
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
    
    @classmethod
    def read_from_json(self, path: str):
        json_file = open(path)
        json_instance = json.loads(json_file.read())
        json_nodes = json_instance["nodes"]
        json_weighted_edges = json_instance["weighted_edges"]
        json_requests = json_instance["requests"]
        json_file.close()

        nodes = dict()
        for json_node in json_nodes:
            node = Node.from_json(json_node)
            nodes[node.id] = node
        weighted_edges = []
        for json_weighted_edge in json_weighted_edges:
            weighted_edge = WeightedEdge.from_json(json_weighted_edge)
            nodes[weighted_edge.id_i_node].add_weighted_edge(weighted_edge)
            weighted_edges.append(weighted_edge)
        requests = []
        for json_request in json_requests:
            requests.append(Request.from_json(json_request))
        
        return Instance(nodes, weighted_edges, requests)
    
    def get_cost_between(self, id_i_node, id_j_node):
        for weighted_edge in self.weighted_edges:
            if (weighted_edge.id_i_node == id_i_node and
                weighted_edge.id_j_node == id_j_node):
                return weighted_edge.weight
    
    def get_node(self, node_id) -> Node:
        return self.nodes[node_id]
    
    def is_delivery_node(self, node_id):
        for request in self.requests:
            if (node_id == request.id_delivery_node):
                return True
        return False
    
    def get_pickup_nodes(self, delivery_node_id):
        pickup_nodes = []
        for request in self.requests:
            if (delivery_node_id == request.id_delivery_node):
                pickup_nodes.append(request.id_pickup_node)
        return pickup_nodes

    def save_to_json(self, path: str):
        with open(path, "w", encoding="utf-8") as output:
            json.dump(self._to_json(), output, ensure_ascii=False, indent=4)

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
        for node in self.nodes.values():
            output += str(node) + "\n"
        output += "WEIGHTED EDGES:\n"
        for weigted_edge in self.weighted_edges:
            output += str(weigted_edge) + "\n"
        output += "REQUESTS:\n"
        for request in self.requests:
            output += str(request) + "\n"
        return output