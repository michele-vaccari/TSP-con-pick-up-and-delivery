
from ..problem.instance import Instance
from ..problem.solution import Solution
from .greedyTemplate import GreedyTemplate
from .greedyRandom import GreedyRandom
from tsppd.solver.largeNeighborhoodSearch import LargeNeighborhoodSearch

import copy

from ..utils.observerPattern import Subject, Observer
from typing import List

class MultiStartLocalSearch(Subject):
    def __init__(self, instance: Instance):
        """
        Multi Start Local Search method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance

        # parameters
        self._max_iterations_number = 10

        self._observers: List[Observer] = []
        self._feasible_solutions_counter = 0
        self._current_solution = None

    @property
    def instance(self):
        return self._instance
    
    @property
    def max_iterations_number(self):
        return self._max_iterations_number
    
    @property
    def feasible_solutions_counter(self):
        return self._feasible_solutions_counter
    
    @property
    def current_solution(self):
        return self._current_solution
    
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

    def _multi_start_local_search(self):
        local_search_solutions = []

        for _ in range(self._max_iterations_number):
            greedyRandom = GreedyRandom()
            greedyTemplate = GreedyTemplate(self._instance, greedyRandom)
            greedyRandomSolution = greedyTemplate.calculate_solution()

            largeNeighborhoodSearch = LargeNeighborhoodSearch(self._instance, greedyRandomSolution)
            largeNeighborhoodSearchSolution = largeNeighborhoodSearch.calculate_solution()

            self._current_solution = largeNeighborhoodSearchSolution
            self._feasible_solutions_counter += 1
            self.notify_new_solution()

            local_search_solutions.append(copy.deepcopy(largeNeighborhoodSearchSolution))
        
        return min(local_search_solutions)

    def calculate_solution(self) -> Solution:
        return self._multi_start_local_search()