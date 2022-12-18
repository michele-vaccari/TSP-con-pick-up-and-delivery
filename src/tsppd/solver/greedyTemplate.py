from ..problem.instance import Instance
from ..problem.solution import Solution

class GreedyTemplate:
    def __init__(self, instance: Instance, greedy):
        """
        Greedy template method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param greedy: object that implements the get_best_admissible_node method
        """
        self._instance = instance
        self._greedy = greedy

    @property
    def instance(self):
        return self._instance
    
    def _compute_greedy(self) -> Solution:
        nodes_to_visit = []
        for node in self.instance.nodes.values():
            nodes_to_visit.append(node.id)
        
        # start with depot node
        self._tour.append(0)
        nodes_to_visit.remove(0)

        while len(nodes_to_visit) > 0:
            best_node = self._greedy.get_best_admissible_node(self._instance, self._tour, nodes_to_visit.copy())
            self._tour.append(best_node)
            nodes_to_visit.remove(best_node)
        
        # end with depot node
        self._tour.append(0)

        return Solution(self.instance, self._tour)

    def calculate_solution(self) -> Solution:
        return self._compute_greedy()
    
    _tour = []