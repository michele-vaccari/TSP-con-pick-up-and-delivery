from ..problem.instance import Instance
from ..problem.solution import Solution

class Enumerator:
    def __init__(self, instance: Instance):
        """
        Solver by enumerative method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance

    @property
    def instance(self):
        return self._instance

    def calculate_solution(self) -> Solution:
        starting_solution_nodes_id = [0] # starting node is the depot node
        best_solution = Solution(self.instance, starting_solution_nodes_id)
        return best_solution