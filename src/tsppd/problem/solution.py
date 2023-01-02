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

        current_node_id_iterator = iter(self.solution_nodes_id)
        next_node_id_iterator = iter(self.solution_nodes_id)
        next(next_node_id_iterator, None)
        while True:
            current_node_id = next(current_node_id_iterator, None)
            if current_node_id == None:
                if cost == 0:
                    return None
                else:
                    return cost
            next_node_id = next(next_node_id_iterator, None)
            if next_node_id == None:
                if cost == 0:
                    return None
                else:
                    return cost
            cost += self.instance.get_cost_between(current_node_id, next_node_id)
    
    def __gt__(self, other):
        if isinstance(other, Solution):
            return self.cost > other.cost
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Solution):
            return self.instance == other.instance and self.solution_nodes_id == other.solution_nodes_id
        return NotImplemented

    def __str__(self):
        output = "SOLUTION NODES ID:\n"
        for solution_node_id in self._solution_nodes_id:
            output += str(solution_node_id) + "\n"
        output += "SOLUTION COST: {}\n".format(self.cost)
        return output