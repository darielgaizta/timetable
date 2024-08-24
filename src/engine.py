"""
Timetable generator engine.
"""

import random
from abc import ABC, abstractmethod
from app.services import RequestRoomTimeslotService

class Engine(ABC):
    EXEC_TIME_LIMIT = 1800

    def __init__(self,
                 rooms: list,
                 timeslots: list,
                 course_classes: list,
                 location_links: list,
                 proposal: list):
        self.rooms = rooms
        self.timeslots = timeslots
        self.course_classes = course_classes
        self.location_links = location_links
        self.proposal = proposal
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
                is_proposed = (course_class1.course.code == course_class2.course.code
                               and any(course_class1.course.code in item for item in self.proposal))
                conflict += self.validate_course_classes(solution, course_class1, course_class2, is_proposed)
        conflict += self.validate_proposal(solution)
        print('### Evaluating conflicts on solution -->', conflict)
        return conflict
    
    def validate_course_classes(self, solution, course_class1, course_class2, is_proposed):
        """Ensure there is no conflict between two course classes."""
        room1, course1, timeslot1, location1 = solution[course_class1].values()
        room2, course2, timeslot2, location2 = solution[course_class2].values()
        timeslot_diffs = abs(int(timeslot1.code[1:]) - int(timeslot2.code[1:]))
        travel_time = self.get_travel_time(location1, location2)

        condition1 = timeslot1 == timeslot2 and room1 == room2
        condition2 = (course1 == course2
                      and timeslot1 != timeslot2)
        condition3 = (course1 != course2
                      and location1 != location2
                      and course_class1.number == course_class2.number)
        condition4 = (course1 != course2
                      and course_class1.number != course_class2.number
                      and course1.semester == course2.semester
                      and travel_time != 0
                      and travel_time >= timeslot_diffs)
        
        conflict = condition1 or condition2 or condition4 if not is_proposed else condition1 or condition4
        return 1 if conflict else 0
    
    def validate_proposal(self, solution):
        service = RequestRoomTimeslotService(solution=solution, proposal=self.proposal)
        matches = service.match()
        conflicts = len(self.proposal) - len(matches)
        if conflicts > 0:
            return conflicts
        return 0
    
    def get_travel_time(self, location1, location2):
        for link in self.location_links:
            if location1 != location2:
                if ((link.location1 == location1 or link.location2 == location1)
                    and (link.location2 == location1 or link.location2 == location2)):
                    return link.travel_time
        return 0
    
    @abstractmethod
    def run(self, *args, **kwargs): pass