"""
Timetable generator engine.
"""

import random
from abc import ABC, abstractmethod

class Engine(ABC):

    def __init__(self,
                 rooms: list,
                 timeslots: list,
                 course_classes: list,
                 location_links: list):
        self.rooms = rooms
        self.timeslots = timeslots
        self.course_classes = course_classes
        self.location_links = location_links
        self.timetable = { course_class: {
            'room': None,
            'course': None,
            'timeslot': None,
            'location': None,
            } for course_class in course_classes }
        self.randomize()
    
    def randomize(self):
        for course_class in self.course_classes:
            self.timetable[course_class]['room'] = random.choice(self.rooms)
            self.timetable[course_class]['course'] = course_class.course
            self.timetable[course_class]['timeslot'] = random.choice(self.timeslots)
            self.timetable[course_class]['location'] = self.timetable[course_class]['room'].location
    
    def evaluate(self, solution: dict):
        conflict = 0
        for i in range(len(self.course_classes) - 1):
            for j in range(i + 1, len(self.course_classes)):
                course_class1 = self.course_classes[i]
                course_class2 = self.course_classes[j]
                conflict += self.validate_course_classes(solution, course_class1, course_class2)
        print('Evaluating conflict -->', conflict)
        return conflict
    
    def validate_course_classes(self, solution, course_class1, course_class2):
        """Ensure there is no conflict between two course classes."""
        room1, course1, timeslot1, location1 = solution[course_class1].values()
        room2, course2, timeslot2, location2 = solution[course_class2].values()
        
        condition1 = timeslot1 == timeslot2 and room1 == room2
        condition2 = (course1.code == course2.code
                      and timeslot1 != timeslot2)
        condition3 = (course1.code != course2.code
                      and location1.code != location2.code
                      and course_class1.number == course_class2.number)
        
        conflict = condition1 or condition2 or condition3
        return 1 if conflict else 0
    
    @abstractmethod
    def run(self, *args, **kwargs): pass