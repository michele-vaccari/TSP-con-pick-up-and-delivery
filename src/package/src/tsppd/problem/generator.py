import random

from .node import Node
from .request import Request
from .instance import Instance

class Generator:
    def __init__(self, nodes_number: int, requests_number: int):
        """
        Instance generator of TSPPD problem.
        :param nodes_number: number of instance nodes
        :param requests_number: number of instance requests
        """
        self._nodes_number = nodes_number
        self._requests_number = requests_number

    @property
    def nodes_number(self):
        return self._nodes_number

    @property
    def requests_number(self):
        return self._requests_number
    
    def generate_instance(self) -> Instance:
        nodes = self._generate_nodes()
        requests = self._generate_requests(nodes)
        return Instance(nodes, requests)
        
    def _generate_nodes(self):
        nodes = []
        for id in range(0, self.nodes_number):
            x = random.randint(0, self.nodes_number**2)
            y = random.randint(0, self.nodes_number**2)
            nodes.append(Node(id,x,y))
        return nodes

    def _generate_requests(self, nodes):
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