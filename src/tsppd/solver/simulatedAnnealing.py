from ..problem.instance import Instance
from ..problem.solution import Solution

import random
import math

class SimulatedAnnealing:
    def __init__(self, instance: Instance, initial_solution: Solution):
        """
        Simulated Annealing method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param initial_solution: initial admissible solution to optimize
        """
        self._instance = instance
        self._initial_solution = initial_solution
        self._initial_temperature = 900
        self._final_temperature = 0.1
        self._cooling_rate = 0.92
        self._iterations_for_temperature = 5

    @property
    def instance(self):
        return self._instance
    
    @property
    def initial_solution(self):
        return self._initial_solution

    def _is_tour_admissible(self, tour):
        for i in range(0, len(tour)):
            subtour = tour[0:i]
            pickup_nodes_of_current_node = self.instance.get_pickup_nodes(tour[i])
            if (self.instance.is_delivery_node(tour[i]) and not(all(node in subtour for node in pickup_nodes_of_current_node))):
                return False
        
        return True
    
    def _random_city_swap(self) -> Solution:
        current_solution_nodes_id = self.initial_solution.solution_nodes_id.copy()

        first_node_position = random.randint(1, len(self.initial_solution.solution_nodes_id) - 1)
        second_node_position = random.randint(1, len(self.initial_solution.solution_nodes_id) - 1)
        current_solution_nodes_id[first_node_position], current_solution_nodes_id[second_node_position] = current_solution_nodes_id[second_node_position], current_solution_nodes_id[first_node_position]

        if self._is_tour_admissible(current_solution_nodes_id):
            return Solution(self.instance, current_solution_nodes_id)
        else:
            return self._random_city_swap()
    
    def _simulated_annealing(self):
        current_temperature = self._initial_temperature
        current_solution = self.initial_solution
        best_solution = current_solution

        while current_temperature > self._final_temperature:
            for _ in range(self._iterations_for_temperature):
                next_solution = self._random_city_swap()
                delta = next_solution.cost - current_solution.cost
                if delta < 0:
                    current_solution = next_solution
                    if current_solution.cost < best_solution.cost:
                        best_solution = next_solution
                else:
                    r = random.uniform(0, 1)
                    if r < math.exp(-delta/current_temperature):
                        current_solution = next_solution
            current_temperature = current_temperature * self._cooling_rate
        return best_solution
    
    def calculate_solution(self) -> Solution:
        return self._simulated_annealing()