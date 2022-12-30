from ..problem.instance import Instance
from ..problem.solution import Solution

import copy
import random

class LargeNeighborhoodSearch:
    def __init__(self, instance: Instance, initial_solution: Solution):
        """
        Large Neighborhood Search method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param initial_solution: initial admissible solution to optimize
        """
        self._instance = instance
        self._initial_solution = initial_solution

        # parameters
        self._destruction_rate = 0.3
        self._k_max = 2
        self._max_number_of_worsening = 100
        self._nodes_to_repair = []

    @property
    def instance(self):
        return self._instance
    
    def _stop_condition(self, k, number_of_worsening):
        return k > self._k_max or number_of_worsening > self._max_number_of_worsening
    
    def _destroy(self, solution: Solution):
        new_solution_nodes_id = copy.copy(solution.solution_nodes_id)
        # remove depot nodes
        del new_solution_nodes_id[0]
        del new_solution_nodes_id[-1]

        number_of_nodes_to_destroy = int(self._destruction_rate * len(new_solution_nodes_id))

        for _ in range(number_of_nodes_to_destroy):
            random_index = random.randrange(len(new_solution_nodes_id))
            self._nodes_to_repair.append(new_solution_nodes_id[random_index])
            del new_solution_nodes_id[random_index]
        
        # restore depot nodes
        new_solution_nodes_id.insert(0, 0)
        new_solution_nodes_id.append(0)

        return Solution(solution.instance, new_solution_nodes_id)

    def _repair(self, partial_solution: Solution):
        pickup_nodes_to_repair = []
        delivery_nodes_to_repair = []
        
        for node in self._nodes_to_repair:
            if self._instance.is_pickup_node(node):
                pickup_nodes_to_repair.append(node)
            elif self._instance.is_delivery_node(node):
                delivery_nodes_to_repair.append(node)
        
        # restore pickup nodes
        best_partial_solution = partial_solution
        current_partial_solution = partial_solution
        for node in pickup_nodes_to_repair:
            if len(best_partial_solution.solution_nodes_id) > len(partial_solution.solution_nodes_id):
                current_partial_solution = best_partial_solution
            delivery_node = self._instance.get_delivery_node(node)
            if delivery_node in current_partial_solution.solution_nodes_id:
                delivery_node_index = current_partial_solution.solution_nodes_id.index(delivery_node)
            else:
                delivery_node_index = len(current_partial_solution.solution_nodes_id)
            for index in range(1, delivery_node_index + 1):
                next_partial_solution_nodes_id = copy.copy(current_partial_solution.solution_nodes_id)
                next_partial_solution_nodes_id.insert(index, node)
                next_partial_solution = Solution(self._instance, copy.copy(next_partial_solution_nodes_id))
                if index == 1 or next_partial_solution.cost < current_partial_solution.cost:
                    best_partial_solution = next_partial_solution

        # restore delivery nodes
        pickup_restored_partial_solution = best_partial_solution
        current_partial_solution = pickup_restored_partial_solution
        for node in delivery_nodes_to_repair:
            if len(best_partial_solution.solution_nodes_id) > len(pickup_restored_partial_solution.solution_nodes_id):
                current_partial_solution = best_partial_solution
            pickup_node = self._instance.get_pickup_node(node)
            pickup_node_index = current_partial_solution.solution_nodes_id.index(pickup_node)
            for index in range(pickup_node_index + 1, len(current_partial_solution.solution_nodes_id)):
                next_partial_solution_nodes_id = copy.copy(current_partial_solution.solution_nodes_id)
                next_partial_solution_nodes_id.insert(index, node)
                next_partial_solution = Solution(self._instance, copy.copy(next_partial_solution_nodes_id))
                if index == (pickup_node_index + 1) or next_partial_solution.cost < current_partial_solution.cost:
                    best_partial_solution = next_partial_solution

        self._nodes_to_repair = []

        return best_partial_solution
    
    def _accept(self, current_solution, k_solution):
        # accetto solo se miglioro
        return current_solution.cost < k_solution.cost

    def _large_neighborhood_search(self):
        initial_solution = self._initial_solution
        k = 0
        number_of_worsening = 0
        k_solution = initial_solution
        best_solution = initial_solution

        while not self._stop_condition(k, number_of_worsening):
            current_solution = self._repair(self._destroy(k_solution))
            if self._accept(current_solution, k_solution):
                k_solution = current_solution
                k = k + 1
            else:
                number_of_worsening = number_of_worsening + 1
            if k_solution.cost < best_solution.cost:
                best_solution = k_solution
                number_of_worsening = 0

        return best_solution
    
    def calculate_solution(self) -> Solution:
        return self._large_neighborhood_search()
