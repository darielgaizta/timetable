from django.db import models

# === Location and Room

class Location(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    
    def __str__(self) -> str:
        return self.code


class Room(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    capacity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.code
    

class LocationLink(models.Model):
    location1 = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location1')
    location2 = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location2')
    travel_time = models.IntegerField()

    def __str__(self) -> str:
        return 'Travel time from {} to {}: {}'.format(
            self.location1.code,
            self.location2.code,
            self.travel_time
        )


# === Course and Class

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True)
    credit = models.IntegerField()
    semester = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.code


class CourseClass(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return '{}-{}'.format(self.course.code, self.number)


# Timeslot

class Timeslot(models.Model):
    code = models.CharField(max_length=3, unique=True)

    def __str__(self) -> str:
        return self.code
    

# Schedule

# class Schedule(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
#     course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.course_class.__str__()
    
#     def unpack(self):
#         return self.room, self.timeslot, self.course_class