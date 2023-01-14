from ..problem.instance import Instance
from ..problem.solution import Solution

from ..utils.observerPattern import Subject, Observer
from typing import List

import itertools

class BruteForceEnumerator(Subject):
    def __init__(self, instance: Instance):
        """
        Solver by brute force enumerative method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance
        self._best_solution = None
        
        self._feasible_solutions_counter = 0
        self._observers: List[Observer] = []

        self._current_solution = None

    @property
    def instance(self):
        return self._instance
    
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

    def _enumerate(self) -> Solution:

        nodes_id = []
        for node in self._instance.nodes.values():
            nodes_id.append(node.id)
        
        nodes_id.remove(0)

        for permutation in itertools.permutations(nodes_id):
            solution = list(permutation)
            solution.insert(0, 0) # depot is start node
            solution.append(0) # depot is end node

            current_solution = []
            solution_is_feasible = True
            for node in solution:
                current_solution.append(node)
                # check if solution is feasible
                pickup_nodes_of_current_node = self.instance.get_pickup_nodes(node)
                if (self.instance.is_delivery_node(node) and not(all(node in current_solution for node in pickup_nodes_of_current_node))):
                    solution_is_feasible = False # appena trovo un'ordine non rispettato scarta tutto l'albero
                    break

            if (solution_is_feasible):
                current_solution = Solution(self.instance, solution.copy())
                self._current_solution = current_solution
                self._feasible_solutions_counter += 1
                self.notify_new_solution()
                if self._best_solution == None or current_solution.cost <= self._best_solution.cost:
                    self._best_solution = current_solution
                    self.notify_best_new_solution()

    def calculate_solution(self) -> Solution:
        self._enumerate()
        return self._best_solution