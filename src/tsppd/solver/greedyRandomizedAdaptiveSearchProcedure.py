
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

        # parameters
        self._max_iterations_number = 10
        self._restricted_candidate_list_items = 2 * self._max_iterations_number
        ## TODO: add path relinking intensification tecnique

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
    
    def _greedy_randomized_adaptive_search_procedure(self):
        restricted_candidate_list = self._build_restricted_candidate_list()
        grasp_solutions = []

        for _ in range(self._max_iterations_number):
            largeNeighborhoodSearch = LargeNeighborhoodSearch(self._instance, random.choice(restricted_candidate_list))
            largeNeighborhoodSearchSolution = largeNeighborhoodSearch.calculate_solution()
            grasp_solutions.append(copy.deepcopy(largeNeighborhoodSearchSolution))
        
        return min(grasp_solutions)

    def calculate_solution(self) -> Solution:
        return self._greedy_randomized_adaptive_search_procedure()