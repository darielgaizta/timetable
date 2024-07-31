"""
Timetable generator engine.
"""

from abc import ABC, abstractmethod

class Engine(ABC):

    def __init__(self, schedules: list, links: list):
        self.schedules = schedules
        self.links = links
    
    def evaluate(self):
        conflict = 0
        for i in range(len(self.schedules)):
            for j in range(i, len(self.schedules)):
                schedule1 = self.schedules[i]
                schedule2 = self.schedules[j]
                conflict += self.validate_schedule(schedule1, schedule2)
        return conflict

    def validate_schedule(self, schedule1, schedule2):
        """Ensure there is no conflict between two schedules."""
        room1, timeslot1, course_class1 = schedule1.unpack()
        room2, timeslot2, course_class2 = schedule2.unpack()

        condition1 = timeslot1 == timeslot2 and room1 == room2
        condition2 = (course_class1.course.code == course_class2.course.code
                      and timeslot1 != timeslot2)
        condition3 = (course_class1.course.code != course_class2.course.code
                      and course_class1.number == course_class2.number
                      and room1.location.code != room2.location.node)
        
        conflict = condition1 or condition2 or condition3
        return 1 if conflict else 0
    
    @abstractmethod
    def run(self, *args, **kwargs): pass