"""Services for internal operations."""

import random
import string
from faker import Faker
from . import models

class DataGeneratorService:
    
    def __init__(self,
                 rooms_dict,
                 nb_courses,
                 nb_timeslots,
                 nb_locations):
        self.faker = Faker()
        self.__rooms = []
        self.__courses = []
        self.__locations = []
        self.__timeslots = []
        # self.course_classes = []
        self.generate_rooms(rooms_dict, nb_locations)
        self.generate_timeslots(nb_timeslots)
        self.generate_courses(nb_courses)

    def generate_code(self, length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def generate_locations(self, nb_locations):
        for _ in range(nb_locations):
            name = self.faker.location_on_land()
            code = self.generate_code(length=3)
            new_location = models.Location(name=name, code=code)
            self.__locations.append(new_location)
    
    def generate_rooms(self, rooms_dict, nb_locations):
        self.generate_locations(nb_locations)
        for i in range(nb_locations):
            nb_rooms = rooms_dict[f'rooms{i + 1}']
            for _ in range(nb_rooms):
                name = self.faker.company()
                code = self.generate_code(length=5)
                capacity = random.randint(40, 100)
                location = self.__locations[i]
                new_room = models.Room(name=name, code=code, capacity=capacity, location=location)
                self.__rooms.append(new_room)
    
    def generate_courses(self, nb_courses):
        for _ in range(nb_courses):
            name = self.faker.country()
            code = self.generate_code(length=6)
            credit = random.randint(2, 5)
            semester = random.choice([1, 3, 5, 7])
            department = self.faker.city()
            new_courses = models.Course(name=name, code=code, credit=credit, semester=semester, department=department)
            self.__courses.append(new_courses)
    
    # def generate_course_classes(self, nb_courses, course_classes_dict):
    #     self.generate_courses(nb_courses)
    #     for course in self.__courses:
    #         nb_course_classes = course_classes_dict[course]
    #         for number in range(1, nb_course_classes + 1):
    #             capacity = random.randint(40, 100)
    #             new_course_class = models.CourseClass(number, course, capacity)
    #             self.course_classes.append(new_course_class)
    
    def generate_timeslots(self, nb_timeslots):
        for _ in range(nb_timeslots):
            code = self.generate_code(length=3)
            new_timeslot = models.Timeslot(code=code)
            self.__timeslots.append(new_timeslot)
        
    def get_rooms(self): return self.__rooms
    def get_courses(self): return self.__courses
    def get_locations(self): return self.__locations
    def get_timeslots(self): return self.__timeslots