import random

from .node import Node
from .weightedEdge import WeightedEdge
from .request import Request
from .instance import Instance

class Generator:
    def __init__(self, nodes_number: int, requests_number: int, weights_are_euclidean_distance: bool):
        """
        Instance generator of TSPPD problem.
        :param nodes_number: number of instance nodes
        :param requests_number: number of instance requests
        :param weights_are_euclidean_distance: weights are the Euclidean distance between nodes
        """
        self._nodes_number = nodes_number
        self._requests_number = requests_number
        self._weights_are_euclidean_distance = weights_are_euclidean_distance
    
    _MAX_TRAVEL_TIME = 100

    @property
    def nodes_number(self):
        return self._nodes_number
    
    @property
    def requests_number(self):
        return self._requests_number
    
    @property
    def weights_are_euclidean_distance(self):
        return self._weights_are_euclidean_distance

    def generate_instance(self) -> Instance:
        nodes = self._generate_nodes()
        weighted_edges = self._generate_weighted_edges(nodes)
        requests = self._generate_requests(nodes)
        return Instance(nodes, weighted_edges, requests)
        
    def _generate_nodes(self):
        nodes = []
        for id in range(0, self.nodes_number):
            x = random.randint(0, self.nodes_number**2)
            y = random.randint(0, self.nodes_number**2)
            nodes.append(Node(id,x,y))
        return nodes
    
    def _generate_weighted_edges(self, nodes: list):
        weighted_edges = []
        for i in nodes:
            id_i_node = i.id
            for j in nodes:
                id_j_node = j.id
                if id_i_node == id_j_node:
                    continue
                weight = self._generate_weight(i, j)
                weighted_edges.append(WeightedEdge(id_i_node, id_j_node, weight))
        return weighted_edges
    
    def _generate_weight(self, i_node: Node, j_node: Node):
        if (self.weights_are_euclidean_distance):
            return i_node.euclidean_distance(j_node)
        return random.randint(1, self._MAX_TRAVEL_TIME)
        

    def _generate_requests(self, nodes: list):
        requests = []
        for id in range(0, self.requests_number):
            while True:
                id_pickup_node = random.randint(1, len(nodes))
                while True:
                    id_delivery_node = random.randint(1, len(nodes))
                    if id_pickup_node != id_delivery_node:
                        break
                request = Request(id_pickup_node, id_delivery_node)
                if request not in requests:
                    requests.append(Request(id_pickup_node, id_delivery_node))
                    break
        return requests