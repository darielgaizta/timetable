"""Services for internal operations."""

import re
import random
import string
from faker import Faker
from . import models

class GeneratorService:
    
    def __init__(self):
        self.faker = Faker()
        self.__rooms = []
        self.__courses = []
        self.__locations = []
        self.__timeslots = []
    
    def generate_data(self, rooms_dict, nb_courses, nb_timeslots, nb_locations, travel_time_dict):
        self.__generate_rooms(rooms_dict, nb_locations)
        self.__generate_timeslots(nb_timeslots)
        self.__generate_courses(nb_courses)
        self.__generate_location_links(travel_time_dict)

    def __generate_code(self, length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def __generate_locations(self, nb_locations):
        for _ in range(nb_locations):
            name = self.faker.location_on_land()
            code = self.__generate_code(length=3)
            new_location = models.Location.objects.create(name=name, code=code)
            self.__locations.append(new_location)
    
    def __generate_rooms(self, rooms_dict, nb_locations):
        self.__generate_locations(nb_locations)
        for i in range(nb_locations):
            nb_rooms = rooms_dict[f'rooms{i + 1}']
            location_room_code = self.__generate_code(length=2)
            for j in range(1, nb_rooms + 1):
                name = self.faker.company()
                code = location_room_code + f'{j:03}'
                capacity = random.randint(40, 100)
                location = self.__locations[i]
                new_room = models.Room.objects.create(name=name, code=code, capacity=capacity, location=location)
                self.__rooms.append(new_room)
    
    def __generate_courses(self, nb_courses):
        for _ in range(nb_courses):
            name = self.faker.country()
            code = self.__generate_code(length=6)
            credit = random.randint(2, 5)
            semester = random.choice([1, 3, 5, 7])
            department = self.faker.city()
            new_courses = models.Course.objects.create(name=name, code=code, credit=credit, semester=semester, department=department)
            self.__courses.append(new_courses)
    
    def __generate_timeslots(self, nb_timeslots):
        for i in range(1, nb_timeslots + 1):
            code = f'T{i:02}'
            new_timeslot = models.Timeslot.objects.create(code=code)
            self.__timeslots.append(new_timeslot)
        
    def __generate_location_links(self, travel_time_dict):
        for k, v in travel_time_dict.items():
            matched = re.search(r'travel_time_(\d+)_(\d+)', k)
            if matched:
                i, j = int(matched.group(1)), int(matched.group(2))
                location1 = self.__locations[i-1]
                location2 = self.__locations[j-1]
                models.LocationLink.objects.create(location1=location1, location2=location2, travel_time=v)
        
    def get_rooms(self): return self.__rooms
    def get_courses(self): return self.__courses
    def get_locations(self): return self.__locations
    def get_timeslots(self): return self.__timeslots


class RequestRoomTimeslotService:
    REQ_ROOM_REGEX = r'req_room_(\w+)_(\w+)'
    REQ_TIMESLOT_REGEX = r'req_timeslot_(\w+)_(\w+)'
    
    def __init__(self, solution, proposal):
        self.solution = solution
        self.proposal = proposal
        self._pairs = []
    
    def parse_proposal(self):
        for i in self.proposal:
            room = re.findall(self.REQ_ROOM_REGEX, i)
            timeslot = re.findall(self.REQ_TIMESLOT_REGEX, i)
            self._pairs += room + timeslot
    
    def match(self):
        matches = {}
        self.parse_proposal()
        for pair in self._pairs:
            matched = {k: v for k, v in self.solution.items()
                       if (v['timeslot'].code == pair[1]
                       or v['room'].code == pair[1])
                       and k.course.code == pair[0]}
            if matched:
                key, value = next(iter(matched.items()))
                matches = matches | {key: value}
        return matches