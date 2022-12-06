from tsppd.problem.node import Node

def test_node_property():
    node = Node(0, 1, 2)
    assert node.id == 0 and node.x == 1 and node.y == 2

def test_node_to_string():
    node = Node(0, 1, 2)
    assert str(node) == "node[0] = (1, 2)"