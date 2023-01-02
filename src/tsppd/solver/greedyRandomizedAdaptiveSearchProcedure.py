
from ..problem.instance import Instance
from ..problem.solution import Solution
from .greedyTemplate import GreedyTemplate
from .greedyRandom import GreedyRandom
from tsppd.solver.largeNeighborhoodSearch import LargeNeighborhoodSearch

import random
import copy

class GreedyRandomizedAdaptiveSearchProcedure:
    def __init__(self, instance: Instance):
        """
        Greedy Randomized Adaptive Search Procedure method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance
        self._path_relinking_best_solutions = []

        # parameters
        self._max_iterations_number = 10
        self._restricted_candidate_list_items = 2 * self._max_iterations_number

    @property
    def instance(self):
        return self._instance
    
    def _build_restricted_candidate_list(self):
        greedy_random_solutions = []

        for _ in range(self._max_iterations_number ** 2):
            greedyRandom = GreedyRandom()
            greedyTemplate = GreedyTemplate(self._instance, greedyRandom)
            greedyRandomSolution = greedyTemplate.calculate_solution()

            greedy_random_solutions.append(copy.deepcopy(greedyRandomSolution))
        
        restricted_candidate_list = []
        for _ in range(self._restricted_candidate_list_items):
            min_solution = min(greedy_random_solutions)
            restricted_candidate_list.append(min_solution)
            greedy_random_solutions.remove(min_solution)
        
        return restricted_candidate_list
    
    def _is_tour_admissible(self, tour):
        for i in range(0, len(tour)):
            subtour = tour[0:i]
            pickup_nodes_of_current_node = self.instance.get_pickup_nodes(tour[i])
            if (self.instance.is_delivery_node(tour[i]) and not(all(node in subtour for node in pickup_nodes_of_current_node))):
                return False
        
        return True

    def _performs_path_relinking(self, initial_solution, guiding_solution):
        # find node to relocate
        nodes_to_relocate = {}
        for index in range(0, len(guiding_solution.solution_nodes_id)):
            if (initial_solution.solution_nodes_id[index] != guiding_solution.solution_nodes_id[index]):
                nodes_to_relocate[index] = guiding_solution.solution_nodes_id[index]
        
        if not nodes_to_relocate:
            return min(self._path_relinking_best_solutions)
        
        # try to relocate
        admissible_solutions = []
        for key, value in nodes_to_relocate.items():
            current_solution = copy.deepcopy(initial_solution)
            current_solution.solution_nodes_id.remove(value)
            current_solution.solution_nodes_id.insert(key, value)
            if (self._is_tour_admissible(current_solution.solution_nodes_id)):
                admissible_solutions.append(current_solution)
        
        best_solution = min(admissible_solutions)
        self._path_relinking_best_solutions.append(copy.deepcopy(best_solution))

        if nodes_to_relocate:
           return self._performs_path_relinking(best_solution, guiding_solution)
    
    def _greedy_randomized_adaptive_search_procedure(self, path_relinking):
        restricted_candidate_list = self._build_restricted_candidate_list()
        grasp_solutions = []

        for _ in range(self._max_iterations_number):
            initial_solution = random.choice(restricted_candidate_list)
            largeNeighborhoodSearch = LargeNeighborhoodSearch(self._instance, initial_solution)
            largeNeighborhoodSearchSolution = largeNeighborhoodSearch.calculate_solution()
            if path_relinking:
                grasp_solutions.append(copy.deepcopy(self._performs_path_relinking(initial_solution, largeNeighborhoodSearchSolution)))
                self._path_relinking_best_solutions = []
            else:
                grasp_solutions.append(copy.deepcopy(largeNeighborhoodSearchSolution))
        
        return min(grasp_solutions)

    def calculate_solution(self, path_relinking) -> Solution:
        return self._greedy_randomized_adaptive_search_procedure(path_relinking)