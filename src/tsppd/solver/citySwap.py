from ..problem.instance import Instance
from ..problem.solution import Solution

from ..utils.observerPattern import Subject, Observer
from typing import List

class CitySwap:
    def __init__(self, instance: Instance, initial_solution: Solution):
        """
        City Swap method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param initial_solution: initial admissible solution to optimize
        """
        self._instance = instance
        self._initial_solution = initial_solution
        self._tour = []

        self._observers: List[Observer] = []
        self._feasible_solutions_counter = 0
        self._current_solution = None
        self._best_solution = None

    @property
    def instance(self):
        return self._instance
    
    @property
    def initial_solution(self):
        return self._initial_solution
    
    @property
    def feasible_solutions_counter(self):
        return self._feasible_solutions_counter
    
    @property
    def current_solution(self):
        return self._current_solution
    
    @property
    def best_solution(self):
        return self._best_solution
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_new_solution(self) -> None:
        for observer in self._observers:
            observer.new_solution_found(self)
    
    def notify_best_new_solution(self) -> None:
        for observer in self._observers:
            observer.new_best_solution_found(self)
    
    def _city_swap(self) -> Solution:
        best_solution = self.initial_solution

        for first_node_position in range(1, len(self.initial_solution.solution_nodes_id) - 1):
            for second_node_position in range(1, len(self.initial_solution.solution_nodes_id) - 1):
                if first_node_position == second_node_position:
                    continue
                current_solution_nodes_id = self.initial_solution.solution_nodes_id.copy()
                current_solution_nodes_id[first_node_position], current_solution_nodes_id[second_node_position] = current_solution_nodes_id[second_node_position], current_solution_nodes_id[first_node_position]

                if self._is_tour_admissible(current_solution_nodes_id):
                    solution = Solution(self.instance, current_solution_nodes_id)
                    self._current_solution = solution
                    self._feasible_solutions_counter += 1
                    self.notify_new_solution()
                    if solution.cost < best_solution.cost:
                        best_solution = solution
                        self._best_solution = best_solution
                        self.notify_best_new_solution()

        return best_solution

    def _is_tour_admissible(self, tour):
        for i in range(0, len(tour)):
            subtour = tour[0:i]
            pickup_nodes_of_current_node = self.instance.get_pickup_nodes(tour[i])
            if (self.instance.is_delivery_node(tour[i]) and not(all(node in subtour for node in pickup_nodes_of_current_node))):
                return False
        
        return True
    
    def calculate_solution(self) -> Solution:
        return self._city_swap()