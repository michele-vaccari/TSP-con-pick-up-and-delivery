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

    def __str__(self):
        return "pickup node id = {} delivery node id = {}".format(self.id_pickup_node, self.id_delivery_node)