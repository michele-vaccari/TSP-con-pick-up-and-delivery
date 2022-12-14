from .instance import Instance

class Solution:
    def __init__(self, instance: Instance, solution_nodes_id: list):
        """
        Instance of TSPPD problem.
        :param instance: TSPPD problem instance
        :param solution_nodes_id: node id list of the solution. The list is an ordered list with FIFO policy.
        """
        self._instances = instance
        self._solution_nodes_id = solution_nodes_id

    @property
    def instance(self):
        return self._instances

    @property
    def solution_nodes_id(self):
        return self._solution_nodes_id
    
    @property
    def cost(self):
        cost = 0

        solution_nodes_id_iterator = iter(self.solution_nodes_id)
        while True:
            current_node_id = next(solution_nodes_id_iterator, None)
            if current_node_id == None:
                if cost == 0:
                    return None
                else:
                    return cost
            next_node_id = next(solution_nodes_id_iterator, None)
            if next_node_id == None:
                if cost == 0:
                    return None
                else:
                    return cost
            cost += self.instance.get_cost_between(current_node_id, next_node_id)
            current_node_id = next_node_id
    
    def __str__(self):
        output = "NODES:\n"
        for node in self.instance.nodes.values():
            output += str(node) + "\n"
        output += "WEIGHTED EDGES:\n"
        for weigted_edge in self.instance.weighted_edges:
            output += str(weigted_edge) + "\n"
        output += "REQUESTS:\n"
        for request in self.instance.requests:
            output += str(request) + "\n"
        output += "SOLUTION NODES ID:\n"
        for solution_node_id in self._solution_nodes_id:
            output += str(solution_node_id) + "\n"
        output += "SOLUTION COST: {}\n".format(self.cost)
        return output