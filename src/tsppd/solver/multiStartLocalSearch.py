
from ..problem.instance import Instance
from ..problem.solution import Solution
from .greedyTemplate import GreedyTemplate
from .greedyRandom import GreedyRandom
from tsppd.solver.largeNeighborhoodSearch import LargeNeighborhoodSearch

import copy

class MultiStartLocalSearch:
    def __init__(self, instance: Instance):
        """
        Multi Start Local Search method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance

        # parameters
        self._max_iterations_number = 10

    @property
    def instance(self):
        return self._instance
    
    def _multi_start_local_search(self):
        local_search_solutions = []

        for _ in range(self._max_iterations_number):
            greedyRandom = GreedyRandom()
            greedyTemplate = GreedyTemplate(self._instance, greedyRandom)
            greedyRandomSolution = greedyTemplate.calculate_solution()

            largeNeighborhoodSearch = LargeNeighborhoodSearch(self._instance, greedyRandomSolution)
            largeNeighborhoodSearchSolution = largeNeighborhoodSearch.calculate_solution()

            local_search_solutions.append(copy.deepcopy(largeNeighborhoodSearchSolution))
        
        return min(local_search_solutions)

    def calculate_solution(self) -> Solution:
        return self._multi_start_local_search()