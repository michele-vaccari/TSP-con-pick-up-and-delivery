from tsppd.problem.generator import Generator

if __name__ == '__main__':
    nodes_number = 10
    requests_number = 20

    generator = Generator(nodes_number, requests_number)
    instance = generator.generate_instance()
    print(instance)