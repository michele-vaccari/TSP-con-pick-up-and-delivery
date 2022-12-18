from tsppd.problem.generator import Generator
from tsppd.problem.instance import Instance
from tsppd.solver.bruteForceEnumerator import BruteForceEnumerator
from tsppd.solver.oneilHoffmanEnumerator import OneilHoffmanEnumerator
from tsppd.solver.greedyTemplate import GreedyTemplate
from tsppd.solver.greedyPickupFirst import GreedyPickupFirst
from tsppd.solver.greedyRequestOrder import GreedyRequestOrder
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--requests', help='Number of requests.', type = click.INT)
@click.option('--weights-as-euclidean-distance/--weights-random', default=False, help='Weights are the Euclidean distance of the nodes / Weights are randomly generated.')
@click.option('--output-instance-path', default=None, help='Path where to save the instance in JSON format.', type = click.STRING)
def generate_instance(requests, weights_as_euclidean_distance, output_instance_path):
    """Generates an instance of the tsppd problem."""
    generator = Generator(requests, weights_as_euclidean_distance)
    instance = generator.generate_instance()
    print(instance)

    if output_instance_path == None:
        return
    
    instance.save_to_json(output_instance_path)

cli.add_command(generate_instance)

@click.command()
@click.option('--input-instance-path', required=True, default=None, help='Path where read the instance in JSON format.', type = click.STRING)
@click.option('--solver-method', required=True, default=None, help='Choose the solver method to use.', type=click.Choice(['brute-force-enumerator', 'oneil-hoffman-enumerator', 'greedy-pickup-first', 'greedy-request-order'], case_sensitive=False))
def solve(input_instance_path, solver_method):
    """Solve an instance of the tsppd problem."""
    print("\n\nREADED INSTANCE\n\n")
    instance = Instance.read_from_json(input_instance_path)
    print(instance)

    if (solver_method == "brute-force-enumerator"):
        enumerator = BruteForceEnumerator(instance)
        solution = enumerator.calculate_solution()
        print("\nBEST SOLUTION: \n")
        print(solution)
    elif (solver_method == "oneil-hoffman-enumerator"):
        enumerator = OneilHoffmanEnumerator(instance)
        solution = enumerator.calculate_solution()
        print("\nBEST SOLUTION: \n")
        print(solution)
    elif (solver_method == "greedy-pickup-first"):
        greedyPickupFirst = GreedyPickupFirst()
        greedyTemplate = GreedyTemplate(instance, greedyPickupFirst)
        solution = greedyTemplate.calculate_solution()
        print("\nGREEDY PICKUP-FIRST SOLUTION: \n")
        print(solution)
    elif (solver_method == "greedy-request-order"):
        greedyRequestOrder = GreedyRequestOrder()
        greedyTemplate = GreedyTemplate(instance, greedyRequestOrder)
        solution = greedyTemplate.calculate_solution()
        print("\nGREEDY REQUEST-ORDER SOLUTION: \n")
        print(solution)

cli.add_command(solve)

if __name__ == '__main__':

    cli()

    # tsppdcli.py generate-instance --requests 10
    # tsppdcli.py generate-instance --requests 10 --weights-random
    # tsppdcli.py generate-instance --requests 10 --weights-as-euclidean-distance
    # tsppdcli.py generate-instance --requests 10 --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-request-weights-random.json
    # tsppdcli.py generate-instance --requests 10 --weights-random --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-request-weights-random.json
    # tsppdcli.py generate-instance --requests 10 --weights-as-euclidean-distance --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-request-weights-euclidean-distance.json
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\2-request-weights-random.json --solver-method brute-force-enumerator
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\2-request-weights-random.json --solver-method oneil-hoffman-enumerator
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\2-request-weights-random.json --solver-method greedy-pickup-first
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\2-request-weights-random.json --solver-method greedy-request-order

    # TODO
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\2-request-weights-random.json --solver-method oneil-hoffman-enumerator --statistics