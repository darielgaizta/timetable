"""
Timetable generator enginge that uses Tabu Search.
"""

import time
import copy
import engine

class TSEngine(engine.Engine):
    
    def __init__(self,
                 rooms: list,
                 timeslots: list,
                 course_classes: list,
                 location_links: list,
                 proposal: list,
                 max_iterations: int,
                 tabu_list_size: int):
        super().__init__(rooms, timeslots, course_classes, location_links, proposal)
        self.tabu_list = []
        self.max_iterations = max_iterations
        self.tabu_list_size = tabu_list_size
    
    def get_neighbors(self, solution):
        neighbors = []
        counter = 1
        for key, value in solution.items():
            print(f'Getting neighbor for {key} => Found: ', end='')
            for room in self.rooms:
                if room != value['room']:
                    for timeslot in self.timeslots:
                        if timeslot != value['timeslot']:
                            neighbor = copy.deepcopy(solution)
                            neighbor[key]['room'] = room
                            neighbor[key]['course'] = key.course
                            neighbor[key]['timeslot'] = timeslot
                            neighbor[key]['location'] = neighbor[key]['room'].location
                            neighbors.append(neighbor)
                            counter += 1
            print(counter)
        return neighbors
    
    def is_tabu(self, solution): return solution in self.tabu_list

    def add_solution_to_tabu(self, solution):
        self.tabu_list.append(solution)
        if len(self.tabu_list) > self.tabu_list_size:
            self.tabu_list.pop(0)
    
    def run(self, *args, **kwargs):
        start_time = time.time()
        iterations = 0

        current_solution = copy.deepcopy(self.timetable)
        current_conflict = self.evaluate(current_solution)
        best_solution = current_solution
        best_score = current_conflict

        while iterations < self.max_iterations:
            checkpoint = time.time()
            print('Checkpoint: Iterations=', iterations)
            if best_score == 0 or checkpoint - start_time > self.EXEC_TIME_LIMIT:
                print('Solution found.') if best_score == 0 else print('Algorithm exceeds time limit.')
                break

            # Add current solution to tabu list.
            self.add_solution_to_tabu(current_solution)

            # Looking for the best neighbor
            best_neighbor = None
            best_conflict = float('inf')
            neighbors = self.get_neighbors(current_solution)

            for neighbor in neighbors:
                if not self.is_tabu(neighbor):
                    score = self.evaluate(neighbor)
                    if score < best_conflict:
                        best_neighbor = neighbor
                        best_conflict = score
            
            # Move searching position to the best neighbor.
            if best_neighbor != None:
                current_solution = best_neighbor
                current_conflict = best_conflict
                
                # Update best solution.
                if current_conflict < best_score:
                    best_solution = current_solution
                    best_score = current_conflict

            iterations += 1
        
        time_taken = time.time() - start_time
        if iterations == self.max_iterations:
            print('Algorithm iterations ended.')
        print('Time taken:', time_taken, 'sec.')
        print(best_solution, '=> Score', best_score)
        return best_solution, best_score, time_taken