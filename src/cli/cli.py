from tsppd.problem.generator import Generator

if __name__ == '__main__':

    # cli.py --generate-instance --nodes 10 --requests 20 --weights-are-euclidean-distance --output-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\instance\10-nodes-20-request-weights-are-euclidean-distance.json

    nodes_number = 10
    requests_number = 20
    weights_are_euclidean_distance = True

    generator = Generator(nodes_number, requests_number, weights_are_euclidean_distance)
    instance = generator.generate_instance()
    print(instance)

    # cli.py --generate-instance --nodes 10 --requests 20

    generator = Generator(nodes_number, requests_number, False)
    instance = generator.generate_instance()
    print(instance)

    # cli.py --generate-instance --nodes 10 --requests 20 --output-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\instance\10-nodes-20-request.json

    # cli.py --instance-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\instance\10-nodes-20-request.json