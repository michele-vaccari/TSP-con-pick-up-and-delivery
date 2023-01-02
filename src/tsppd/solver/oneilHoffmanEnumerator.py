from ..problem.instance import Instance
from ..problem.solution import Solution

class OneilHoffmanEnumerator:
    def __init__(self, instance: Instance):
        """
        Solver by enumerative method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance
        self._tour = []
        self._best_solution = None

    @property
    def instance(self):
        return self._instance

    def _initialize(self):
        for node in self._instance.nodes.values():
            node.sort_weighted_edges_by_ascending_weight()
        self._tour = [0] # starting node is the depot node
    
    def _enumerate(self) -> Solution:
        last_node_of_current_solution = self.instance.get_node(self._tour[-1])
        for weighted_edge in last_node_of_current_solution.weighted_edges:

            # il nodo è già nella soluzione
            if (weighted_edge._id_j_node in self._tour):
                continue

            # aggiungendo il nodo ho un costo della soluzione maggiore del migliore trovato
            current_solution_cost = Solution(self.instance, self._tour).cost
            if (self._best_solution != None and
                current_solution_cost != None and
                current_solution_cost + weighted_edge.weight >= self._best_solution.cost):
                continue
            
            # aggiungendo il nodo violo le precedenze con pickup and delivery
            pickup_nodes_of_id_j_node = self.instance.get_pickup_nodes(weighted_edge._id_j_node)
            if (self.instance.is_delivery_node(weighted_edge._id_j_node) and
                not(all(node in self._tour for node in pickup_nodes_of_id_j_node))):
                continue
            
            self._tour.append(weighted_edge._id_j_node)

            if len(self._tour) >= len(self.instance.nodes):
                solution = self._tour.copy()
                solution.append(0) # ending node is the depot node
                current_solution = Solution(self.instance, solution)
                self._feasible_solutions_counter += 1
                print("Feasible solution: " + str(self._feasible_solutions_counter) + "\n")
                if self._best_solution == None or current_solution.cost <= self._best_solution.cost:
                    self._best_solution = current_solution
            else:
                self._enumerate()
            
            del self._tour[-1]
        
        return self._best_solution

    def calculate_solution(self) -> Solution:
        self._initialize()
        best_solution = self._enumerate()
        return best_solution
    
    _feasible_solutions_counter = 0