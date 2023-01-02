from copy import copy
from ..problem.instance import Instance
from ..problem.solution import Solution

from collections import deque

class TabuSearch:
    def __init__(self, instance: Instance, initial_solution: Solution):
        """
        Tabu Search method of the TSPPD problem.
        :param instance: TSPPD problem instance
        :param initial_solution: initial admissible solution to optimize
        """
        self._instance = instance
        self._initial_solution = initial_solution
        self._tabu_list = deque([], 20) # memorizzo le mosse proibite, se scambio due nodi (34 e 37) allora le mosse da memorizzare sono [34,37] e [37,34]

        self._next_solution_move = None

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
    
    def _city_swap(self, initial_solution) -> Solution:
        best_solution = None

        for first_node_position in range(1, len(initial_solution.solution_nodes_id) - 1):
            for second_node_position in range(1, len(initial_solution.solution_nodes_id) - 1):
                if first_node_position == second_node_position:
                    continue
                
                current_solution_nodes_id = initial_solution.solution_nodes_id.copy()
                current_solution_nodes_id[first_node_position], current_solution_nodes_id[second_node_position] = current_solution_nodes_id[second_node_position], current_solution_nodes_id[first_node_position]

                if current_solution_nodes_id == initial_solution.solution_nodes_id:
                    continue
                
                tabu_move = TabuMove(first_node_position, second_node_position)
                if tabu_move in self._tabu_list:
                    continue

                if self._is_tour_admissible(current_solution_nodes_id):
                    solution = Solution(self.instance, current_solution_nodes_id)
                    if best_solution == None or solution.cost <= best_solution.cost:
                        self._next_solution_move = copy(tabu_move)
                        best_solution = solution

        return best_solution
    
    def _stopping_condition(self, k, stall):
        return k == 20 or stall == 20 # |R|=10
        # return k == 3 or stall == 3 # |R|=30

    def _tabu_search(self):
        # step 1
        k = 1
        current_solution = self.initial_solution
        best_solution = current_solution

        # step 2: explore neighborhood
        stop = False
        stall = 0
        while not stop:
            next_solution = self._city_swap(current_solution)
            #if next_solution == current_solution:
            #    stall = stall + 1
            if next_solution.cost < best_solution.cost:
                stall = 0
                best_solution = next_solution
                current_solution = next_solution
                # step 3: stop or loop
                k = k + 1
                if self._stopping_condition(k, stall):
                    stop = True
                    return best_solution
                else:
                    continue
            if self._next_solution_move in self._tabu_list:
                continue
            else:
                current_solution = next_solution
                stall = stall + 1
                if self._next_solution_move != None:
                    self._tabu_list.append(copy(self._next_solution_move))
                    self._next_solution_move = None
            # step 3: stop or loop
            k = k + 1
            if self._stopping_condition(k, stall):
                stop = True
                return best_solution
            else:
                continue
    

    def calculate_solution(self) -> Solution:
        return self._tabu_search()

class TabuMove:
    def __init__(self, swap_from_node_id, swap_to_node_id):
        """
        Tabu Move for Tabu Search method of the TSPPD problem.
        :param swap_from_node_id:
        :param swap_to_node_id:
        """
        self._swap_from_node_id = swap_from_node_id
        self._swap_to_node_id = swap_to_node_id

    @property
    def swap_from_node_id(self):
        return self._swap_from_node_id
    
    @property
    def swap_to_node_id(self):
        return self._swap_to_node_id
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, TabuMove):
            return (self.swap_from_node_id == other.swap_from_node_id and self.swap_to_node_id == other.swap_to_node_id) or (self.swap_from_node_id == other.swap_to_node_id and self.swap_to_node_id == other.swap_from_node_id)
        return NotImplemented