"""
Timetable generator engine.
"""

from abc import ABC, abstractmethod

class Engine(ABC):

    def __init__(self,
                 rooms: list,
                 classes: list,
                 timeslots: list,
                 timetable: list):
        self.rooms = rooms
        self.classes = classes
        self.timeslots = timeslots
        self.timetable = timetable