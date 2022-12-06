from tsppd.problem.request import Request

def test_request_property():
    request = Request(1, 2)
    assert request.id_pickup_node == 1 and request.id_delivery_node == 2

def test_request_to_string():
    request = Request(1, 2)
    assert str(request) == "(1, 2)"