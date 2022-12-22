from ..problem.instance import Instance
from ..problem.solution import Solution

class CityInsert:
    def __init__(self, instance: Instance, initial_solution: Solution):
        """
        City Insert method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param initial_solution: initial admissible solution to optimize
        """
        self._instance = instance
        self._initial_solution = initial_solution
        self._tour = []

    @property
    def instance(self):
        return self._instance
    
    @property
    def initial_solution(self):
        return self._initial_solution
    
    def _city_insert(self) -> Solution:
        best_solution = self.initial_solution

        for delete_node_position in range(1, len(self.initial_solution.solution_nodes_id) - 1):
            for restore_node_position in range(1, len(self.initial_solution.solution_nodes_id) - 1):
                if delete_node_position == restore_node_position:
                    continue
                current_solution_nodes_id = self.initial_solution.solution_nodes_id.copy()
                node_id = current_solution_nodes_id[delete_node_position]
                del current_solution_nodes_id[delete_node_position]
                current_solution_nodes_id.insert(restore_node_position, node_id)

                if self._is_tour_admissible(current_solution_nodes_id):
                    solution = Solution(self.instance, current_solution_nodes_id)
                    if solution.cost < best_solution.cost:
                        best_solution = solution

        return best_solution

    def _is_tour_admissible(self, tour):
        for i in range(0, len(tour)):
            subtour = tour[0:i]
            pickup_nodes_of_current_node = self.instance.get_pickup_nodes(tour[i])
            if (self.instance.is_delivery_node(tour[i]) and not(all(node in subtour for node in pickup_nodes_of_current_node))):
                return False
        
        return True
    
    def calculate_solution(self) -> Solution:
        return self._city_insert()