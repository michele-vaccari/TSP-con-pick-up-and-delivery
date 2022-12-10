from tsppd.problem.weightedEdge import WeightedEdge

def test_weighted_edge_property():
    weighted_edge = WeightedEdge(0, 1, 2)
    assert weighted_edge.id_i_node == 0 and weighted_edge.id_j_node == 1 and weighted_edge.weight == 2

def test_node_to_string():
    weighted_edge = WeightedEdge(0, 1, 2)
    assert str(weighted_edge) == "(0, 1, 2)"