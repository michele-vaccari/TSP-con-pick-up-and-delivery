class Request:
    def __init__(self, id_pickup_node: int, id_delivery_node: int):
        """
        Create request for TSPPD problem.
        :param id_pickup_node: pickup node id
        :param id_pickup_node: delivery node id
        """
        self._id_pickup_node = id_pickup_node
        self._id_delivery_node = id_delivery_node

    @property
    def id_pickup_node(self):
        return self._id_pickup_node

    @property
    def id_delivery_node(self):
        return self._id_delivery_node
    
    def to_json(self):
        return { "id_pickup_node": self.id_pickup_node, "id_delivery_node": self.id_delivery_node }

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Request):
            return self.id_pickup_node == other.id_pickup_node and self.id_delivery_node == other.id_delivery_node
        return NotImplemented

    def __str__(self):
        return "({}, {})".format(self.id_pickup_node, self.id_delivery_node)