class GreedyPickupFirst:

    @classmethod
    def get_best_admissible_node(self, instance, tour, nodes_to_visit):
        best_node_id = self._get_best_node(instance, nodes_to_visit)
        if (self._is_partial_solution_admissible(instance, best_node_id, tour)):
            return best_node_id
        else:
            nodes_to_visit.remove(best_node_id)
            return self.get_best_admissible_node(instance, tour, nodes_to_visit)
    
    def _get_best_node(instance, nodes_to_visit):
        # first return pickup node
        for node in nodes_to_visit:
            if (instance.is_pickup_node(node)):
                return node
        # then return delivery node
        for node in nodes_to_visit:
            if (instance.is_delivery_node(node)):
                return node
        return None

    def _is_partial_solution_admissible(instance, node_id, tour):
        # check if solution is feasible
        pickup_nodes_of_current_node = instance.get_pickup_nodes(node_id)
        if (instance.is_delivery_node(node_id) and not(all(node in tour for node in pickup_nodes_of_current_node))):
            return False
        else:
            return True