import random

from .node import Node
from .weightedEdge import WeightedEdge
from .request import Request
from .instance import Instance

class Generator:
    def __init__(self, requests_number: int, weights_are_euclidean_distance: bool):
        """
        Instance generator of TSPPD problem.
        :param requests_number: number of instance requests
        :param weights_are_euclidean_distance: weights are the Euclidean distance between nodes
        """
        self._requests_number = requests_number
        self._weights_are_euclidean_distance = weights_are_euclidean_distance
    
    _MAX_TRAVEL_TIME = 100
    
    @property
    def requests_number(self):
        return self._requests_number
    
    @property
    def weights_are_euclidean_distance(self):
        return self._weights_are_euclidean_distance

    def generate_instance(self) -> Instance:
        depot_node_id = 0
        depot_node = self._generate_node(depot_node_id)
        self._nodes[depot_node_id] = depot_node
        requests = self._generate_requests()
        weighted_edges = self._generate_weighted_edges()
        for weighted_edge in weighted_edges:
            self._nodes[weighted_edge.id_i_node].add_weighted_edge(weighted_edge)
        return Instance(self._nodes, weighted_edges, requests)
        
    def _generate_node(self, node_id: int) -> Node:
        x = random.randint(0, self.requests_number**2)
        y = random.randint(0, self.requests_number**2)
        return Node(node_id,x,y)
    
    def _generate_weighted_edges(self):
        weighted_edges = []
        for i in self._nodes.values():
            id_i_node = i.id
            for j in self._nodes.values():
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
        

    def _generate_requests(self):
        requests = []
        pickup_node_id_start = 1
        pickup_node_id_end = self.requests_number + 1
        for pickup_node_id in range(pickup_node_id_start, pickup_node_id_end):
            pickup_node = self._generate_node(pickup_node_id)
            self._nodes[pickup_node.id] = pickup_node
            delivery_node_id = pickup_node_id_end + pickup_node_id - 1
            delivery_node = self._generate_node(delivery_node_id)
            self._nodes[delivery_node.id] = delivery_node
            request = Request(pickup_node.id, delivery_node.id)
            requests.append(request)

        return requests
    
    _nodes = {}