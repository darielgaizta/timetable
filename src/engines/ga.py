"""
Timetable generator engine that uses Genetic Algorithm.
"""

import time
import copy
import random
import engine

class GAEngine(engine.Engine):
    
    def __init__(self,
                 rooms: list,
                 timeslots: list,
                 course_classes: list,
                 location_links: list,
                 proposal: list,
                 num_generations: int,
                 population_size: int):
        super().__init__(rooms, timeslots, course_classes, location_links, proposal)
        self.num_generations = num_generations
        self.population_size = population_size
    
    def perform_crossover(self, parent1, parent2):
        """Returns a new solution which courses are assigned randomly by 50% probability."""
        offspring = {}
        for course_class in self.course_classes:
            if random.random() < 0.5:
                offspring[course_class] = copy.deepcopy(parent1[course_class])
            else:
                offspring[course_class] = copy.deepcopy(parent2[course_class])
        return offspring
    
    def perform_mutation(self, solution):
        """Randomly assign a course class, represents a random mutation."""
        mutated_solution = copy.deepcopy(solution)
        course_class = random.choice(self.course_classes)
        mutated_solution[course_class]['room'] = random.choice(self.rooms)
        mutated_solution[course_class]['course'] = course_class.course
        mutated_solution[course_class]['timeslot'] = random.choice(self.timeslots)
        mutated_solution[course_class]['location'] = mutated_solution[course_class]['room'].location
        return mutated_solution

    def run(self, *args, **kwargs):
        start_time = time.time()
        population = [copy.deepcopy(self.timetable) for _ in range(self.population_size)]
        iterations = 0

        best_solution = min(population, key=lambda s: self.evaluate(s))
        best_score = self.evaluate(best_solution)
        
        while iterations < self.num_generations:
            checkpoint = time.time()
            if best_score == 0 or checkpoint - start_time > self.EXEC_TIME_LIMIT:
                print('Solution found.') if best_score == 0 else print('Algorithm exceeds time limit.')
                break
            
            fitness_scores = [self.evaluate(solution) for solution in population]
            sorted_fitness = sorted(fitness_scores)

            # Select parents to perform crossover.
            parent1 = population[fitness_scores.index(sorted_fitness[0])]
            parent2 = population[fitness_scores.index(sorted_fitness[1])]

            # Perform crossover and mutation.
            new_population = [self.perform_crossover(parent1, parent2) for _ in range(self.population_size)]
            new_population = [self.perform_mutation(solution) if random.random() < 0.2 else solution for solution in new_population]
            population = new_population

            best_solution = min(population, key=lambda solution: self.evaluate(solution))
            best_score = self.evaluate(best_solution)
            iterations += 1

        time_taken = time.time() - start_time
        if iterations == self.num_generations:
            print('Algorithm iterations ended.')
        print('Time taken:', time_taken, 'sec.')
        print(best_solution, '=> Score', best_score)
        return best_solution, best_score, time_taken