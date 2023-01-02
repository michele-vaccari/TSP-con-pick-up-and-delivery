from tsppd.problem.node import Node

def test_node_property():
    node = Node(0, 1, 2)
    assert node.id == 0 and node.x == 1 and node.y == 2

def test_node_to_string():
    node = Node(0, 1, 2)
    assert str(node) == "node[0] = (1, 2)"

def test_node_euclidean_distance():
    node = Node(0, 9, 5)
    other_node = Node(0, 17, 1)
    assert node.euclidean_distance(other_node) == round(float(8.94), 2)