"""
Timetable generator engine that uses Genetic Algorithm.
"""

import engine

class GAEngine(engine.Engine):
    
    def __init__(self,
                 schedules: list,
                 links: list,
                 population_size: int,
                 num_generations: int):
        super().__init__(schedules, links)
        self.population_size = population_size
        self.num_generations = num_generations