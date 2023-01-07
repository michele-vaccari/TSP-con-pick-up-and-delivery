import copy
from ..problem.instance import Instance
from ..problem.solution import Solution
from .greedyTemplate import GreedyTemplate
from .greedyRandom import GreedyRandom

import numpy as np
from datetime import datetime

from ..utils.observerPattern import Subject, Observer
from typing import List

class GeneticAlgoritm(Subject):
    def __init__(self, instance: Instance):
        """
        Genetic Algoritm method of the TSPPD problem.
        :param instance: TSPPD problem instance
        """
        self._instance = instance
        
        # Parameters
        self._n_population = len(instance.nodes) ** 2
        self._mutation_rate = 0.3
        self._max_iteration = 2 * self._n_population

        self._observers: List[Observer] = []
        self._iteration_counter = 0
        self._current_solution = None
        self._best_solution = None

    @property
    def instance(self):
        return self._instance
    
    @property
    def n_population(self):
        return self._n_population
    
    @property
    def mutation_rate(self):
        return self._mutation_rate
    
    @property
    def max_iteration(self):
        return self._max_iteration
    
    @property
    def iteration_counter(self):
        return self._iteration_counter
    
    @property
    def current_solution(self):
        return self._current_solution
    
    @property
    def best_solution(self):
        return self._best_solution
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_new_solution(self) -> None:
        for observer in self._observers:
            observer.new_solution_found(self)
    
    def notify_best_new_solution(self) -> None:
        for observer in self._observers:
            observer.new_best_solution_found(self)

    def _is_tour_admissible(self, tour):
        for i in range(0, len(tour)):
            subtour = tour[0:i]
            pickup_nodes_of_current_node = self.instance.get_pickup_nodes(tour[i])
            if (self.instance.is_delivery_node(tour[i]) and not(all(node in subtour for node in pickup_nodes_of_current_node))):
                return False
        
        return True
    
    # First step: Create the first population set
    def _genesis(self, n_population):
        population_set = []
        greedyRandom = GreedyRandom()
        for _ in range(n_population):
            #Randomly generating a new solution
            greedyTemplate = GreedyTemplate(self._instance, greedyRandom)
            greedyRandomSolution = greedyTemplate.calculate_solution()
            population_set.append(greedyRandomSolution)
        return population_set
    
    def _get_all_fitnes(self, population_set):
        fitnes_list = []
        #Looping over all solutions computing the fitness for each solution
        for i in  range(len(population_set)):
            fitnes_list[i] = population_set[i].cost
        return fitnes_list
    
    # 3. Progenitors selection
    def _progenitor_selection(self, population_set):
        # roulette wheel
        total_fit = sum(solution.cost for solution in population_set)
        prob_list = []
        for solution in population_set:
            prob_list.append(solution.cost/total_fit)
        #prob_list = (solution.cost/total_fit for solution in population_set)

        #Notice there is the chance that a progenitor. mates with oneself
        # sono gli indici delle soluzioni corrispondenti
        progenitor_list_a = np.random.choice(population_set, len(population_set),p=prob_list, replace=True)
        progenitor_list_b = np.random.choice(population_set, len(population_set),p=prob_list, replace=True)
        
        return np.array([progenitor_list_a,progenitor_list_b])
    
    # 4. Mating accoppiamento
    def _mate_progenitors(self, prog_a, prog_b):
        middle_element = int(len(prog_a.solution_nodes_id) / 2)
        prog_a_sx = prog_a.solution_nodes_id[0:middle_element]
        prog_a_dx = prog_a.solution_nodes_id[middle_element:]
        prog_b_sx = prog_b.solution_nodes_id[0:middle_element]
        prog_b_dx = prog_b.solution_nodes_id[middle_element:]

        offspring_sx = prog_a_sx

        # fix offspring dx
        prog_b_dx_duplicate_node_indexes = []
        for i, node in enumerate(prog_b_dx):
            if node == 0:
                continue
            if node in offspring_sx:
                prog_b_dx_duplicate_node_indexes.append(i)
        
        prog_b_dx_missing_values = []
        for node in prog_a_dx:
            if node not in prog_b_dx:
                prog_b_dx_missing_values.append(node)
        
        # create offspring dx
        offspring_dx = copy.copy(prog_b_dx)

        # fix delivery node
        for node in prog_b_sx:
            if node in prog_b_dx_missing_values:
                if self._instance.is_delivery_node(node):
                    offspring_dx[prog_b_dx_duplicate_node_indexes.pop(0)] = node
        # remove unused delivery node
        for index in reversed(prog_b_dx_duplicate_node_indexes):
            del offspring_dx[index]
        
        # fix pickup node
        offset = 0
        for node in prog_b_sx:
            if node in prog_b_dx_missing_values:
                if self._instance.is_pickup_node(node):
                    offspring_dx.insert(0 + offset, node)
                    offset = offset + 1
        
        return Solution(self._instance, (offspring_sx + offspring_dx))
        
    def _mate_population(self, progenitor_list):
        new_population_set = []
        for i in range(progenitor_list.shape[1]):
            prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
            offspring = self._mate_progenitors(prog_a, prog_b)
            new_population_set.append(offspring)
            
        return new_population_set
    
    # 5. Mutation
    def _city_swap(self, initial_solution) -> Solution:

        for first_node_position in range(1, len(initial_solution.solution_nodes_id) - 1):
            for second_node_position in range(1, len(initial_solution.solution_nodes_id) - 1):
                if first_node_position == second_node_position:
                    continue
                current_solution_nodes_id = initial_solution.solution_nodes_id.copy()
                current_solution_nodes_id[first_node_position], current_solution_nodes_id[second_node_position] = current_solution_nodes_id[second_node_position], current_solution_nodes_id[first_node_position]

                if self._is_tour_admissible(current_solution_nodes_id):
                    return Solution(self.instance, current_solution_nodes_id)

    def _mutate_offspring(self, offspring):
        for _ in range(int(len(offspring.solution_nodes_id) * self._mutation_rate)):
            offspring = self._city_swap(offspring)

        return offspring

    def _mutate_population(self, new_population_set):
        mutated_pop = []
        for offspring in new_population_set:
            mutated_pop.append(self._mutate_offspring(offspring))
        return mutated_pop
    
    def _genetic_algoritm(self):
        population_set = self._genesis(self._n_population)
        #fitnes_list = self._get_all_fitnes(population_set)
        progenitor_list = self._progenitor_selection(population_set)
        new_population_set  = self._mate_population(progenitor_list)
        mutated_pop = self._mutate_population(new_population_set)

        best_solution = [-1,np.inf,np.array([])]
        for i in range(self._max_iteration):
            min_solution = min(mutated_pop)

            self._current_solution = min_solution
            self._iteration_counter += 1
            self.notify_new_solution()

            min_solution_cost = min_solution.cost
            # mean_solution_cost = np.mean([solution.cost for solution in mutated_pop])
            #mean_solution_cost = statistics.median(population_set)

            # if i%10==0: print(i, min_solution_cost, mean_solution_cost, datetime.now().strftime("%d/%m/%y %H:%M"))
            #fitnes_list = self.get_all_fitnes(mutated_pop,self._cities_dict)
            
            #Saving the best solution
            if min_solution_cost < best_solution[1]:
                best_solution[0] = i # a che iterazione l'ho trovata
                best_solution[1] = min_solution_cost # qual è il valore di fitness
                best_solution[2] = min_solution # dammi l'ordine di visita dei nodi

                self._best_solution = min_solution
                self.notify_best_new_solution()
            
            progenitor_list = self._progenitor_selection(population_set)
            new_population_set = self._mate_population(progenitor_list)
            
            mutated_pop = self._mutate_population(new_population_set)
        
        #print("Best solution:\n")
        #print("Found at iteration: " + str(best_solution[0]) + "\n")
        #print("With cost: " + str(best_solution[1]) + "\n")

        return best_solution[2]
    
    def calculate_solution(self) -> Solution:
        # 50 minuti per 10 richieste
        return self._genetic_algoritm()