from tsppd.problem.generator import Generator
from tsppd.problem.instance import Instance
from tsppd.solver.enumerator import Enumerator
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--nodes', help='Number of nodes.', type = click.INT)
@click.option('--requests', help='Number of requests.', type = click.INT)
@click.option('--weights-as-euclidean-distance/--weights-random', default=False, help='Weights are the Euclidean distance of the nodes / Weights are randomly generated.')
@click.option('--output-instance-path', default=None, help='Path where to save the instance in JSON format.', type = click.STRING)
def generate_instance(nodes, requests, weights_as_euclidean_distance, output_instance_path):
    """Generates an instance of the tsppd problem."""
    generator = Generator(nodes, requests, weights_as_euclidean_distance)
    instance = generator.generate_instance()
    print(instance)

    if output_instance_path == None:
        return
    
    instance.save_to_json(output_instance_path)

cli.add_command(generate_instance)

@click.command()
@click.option('--input-instance-path', required=True, default=None, help='Path where read the instance in JSON format.', type = click.STRING)
@click.option('--solver-method', required=True, default=None, help='Choose the solver method to use.', type=click.Choice(['enumerator'], case_sensitive=False))
def solve(input_instance_path, solver_method):
    """Solve an instance of the tsppd problem."""
    print("\n\nREADED INSTANCE\n\n")
    instance = Instance.read_from_json(input_instance_path)
    print(instance)

    if (solver_method == "enumerator"):
        enumerator = Enumerator(instance)
        solution = enumerator.calculate_solution()
        print(solution)

cli.add_command(solve)

if __name__ == '__main__':

    cli()

    # tsppdcli.py generate-instance --nodes 10 --requests 20
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-random
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-as-euclidean-distance
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-nodes-20-request-weights-random.json
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-random --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-nodes-20-request-weights-random.json
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-as-euclidean-distance --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-nodes-20-request-weights-euclidean-distance.json

    # TODO
    # tsppdcli.py solve --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\instances\10-nodes-20-request-weights-random.json --solver-method enumerator