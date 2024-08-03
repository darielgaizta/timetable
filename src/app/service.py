"""Services for internal operations."""

import random
import string
from faker import Faker
from . import models

class DataGeneratorService:
    
    def __init__(self):
        self.faker = Faker()
        self.rooms = []
        self.courses = []
        self.locations = []
        self.timeslots = []
        self.course_classes = []

    def generate_code(self, length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def generate_locations(self, nb_locations):
        for _ in range(nb_locations):
            name = self.faker.location_on_land()
            code = self.generate_code(length=3)
            new_location = models.Location(name, code)
            self.locations.append(new_location)
    
    def generate_rooms(self, nb_rooms, nb_locations):
        self.generate_locations(nb_locations)
        for _ in range(nb_rooms):
            name = self.faker.place_name()
            code = self.generate_code(length=5)
            capacity = random.randint(40, 100)
            location = random.choice(self.locations)
            new_room = models.Room(name, code, capacity, location)
            self.rooms.append(new_room)
    
    def generate_courses(self, nb_courses):
        for _ in range(nb_courses):
            name = self.faker.country()
            code = self.generate_code(length=6)
            credit = random.randint(2, 5)
            semester = random.choice([1, 3, 5, 7])
            department = self.faker.department()
            new_courses = models.Course(name, code, credit, semester, department)
            self.courses.append(new_courses)
    
    def generate_course_classes(self, nb_courses, course_classes_dict):
        self.generate_courses(nb_courses)
        for course in self.courses:
            number = course_classes_dict[course]
            capacity = random.randint(40, 100)
            new_course_class = models.CourseClass(number, course, capacity)
            self.course_classes.append(new_course_class)
    
    def generate_timeslots(self, nb_timeslots):
        for _ in range(nb_timeslots):
            code = self.generate_code(length=3)
            new_timeslot = models.Timeslot(code)
            self.timeslots.append(new_timeslot)