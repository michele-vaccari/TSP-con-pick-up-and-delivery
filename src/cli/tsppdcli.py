from tsppd.problem.generator import Generator
from tsppd.problem.instance import Instance
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--nodes', help='Number of nodes.', type = click.INT)
@click.option('--requests', help='Number of requests.', type = click.INT)
@click.option('--weights-as-euclidean-distance/--weights-random', default=False, help='Weights are the Euclidean distance of the nodes / Weights are randomly generated.')
@click.option('--output-instance-path', help='Path where to save the instance in JSON format.', type = click.STRING)
def generate_instance(nodes, requests, weights_as_euclidean_distance, output_instance_path):
    """Generates an instance of the tsppd problem."""
    generator = Generator(nodes, requests, weights_as_euclidean_distance)
    instance = generator.generate_instance()
    print(instance)

    if output_instance_path:
        instance.save_to_json(output_instance_path)
    
    print("\n\nSAVED INSTANCE\n\n")
    saved_instance = Instance.read_from_json(output_instance_path)
    print(saved_instance)

cli.add_command(generate_instance)

if __name__ == '__main__':

    cli()

    # tsppdcli.py generate-instance --nodes 10 --requests 20
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-random
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-as-euclidean-distance
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\10-nodes-20-request-weights-random.json
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-random --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\10-nodes-20-request-weights-random.json
    # tsppdcli.py generate-instance --nodes 10 --requests 20 --weights-as-euclidean-distance --output-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\10-nodes-20-request-weights-euclidean-distance.json

    # TODO
    # tsppdcli.py --input-instance-path C:\dev\TSP-con-pick-up-and-delivery\src\cli\instance\10-nodes-20-request.json