import time
import random
from django.shortcuts import render, redirect
from engines.ga import GAEngine
from utils.excel import Excel
from utils.yaml import Yaml
from utils.serializer import ModelToDictSerializer
from . import models, services

# Create your views here.
def step_1(request):
    if request.method == 'POST':
        request.session['nb_courses'] = int(request.POST['courses'])
        request.session['nb_timeslots'] = int(request.POST['timeslots'])
        request.session['nb_locations'] = int(request.POST['locations'])
        return redirect('step_2')
    
    return render(request, 'views/step_1.html')

def step_2(request):
    context = {
        'nb_courses': range(1, int(request.session['nb_courses']) + 1),
        'nb_timeslots': range(1, int(request.session['nb_timeslots']) + 1),
        'nb_locations': range(1, int(request.session['nb_locations']) + 1),
    }
    
    if request.method == 'POST':
        request.session['search_space'] = int(request.POST['search_space'])
        request.session['iterations'] = int(request.POST['iterations'])
        request.session['rooms_dict'] = {f'rooms{i}': int(request.POST[f'rooms{i}']) for i in context['nb_locations']}
        request.session['travel_time_dict'] = {f'travel_time_{i}_{j}': int(request.POST[f'travel_time_{i}_{j}'])
                                               for i in range(1, int(request.session['nb_locations']))
                                               for j in range(i + 1, int(request.session['nb_locations']) + 1)}
        
        service = services.GeneratorService()
        service.generate_data(
            rooms_dict=request.session['rooms_dict'],
            nb_courses=request.session['nb_courses'],
            nb_timeslots=request.session['nb_timeslots'],
            nb_locations=request.session['nb_locations'],
            travel_time_dict=request.session['travel_time_dict']
        )

        return redirect('step_3')
        
    return render(request, 'views/step_2.html', context)

def step_3(request):
    rooms = models.Room.objects.all()
    courses = models.Course.objects.all()
    timeslots = models.Timeslot.objects.all()
    
    context = {
        'rooms': rooms,
        'courses': courses,
        'timeslots': timeslots
        }

    if request.method == 'POST':
        for course in courses:
            credit = int(request.POST.get(f'credit{course.code}'))
            semester = int(request.POST.get(f'semester{course.code}'))
            nb_classes = int(request.POST.get(f'nb_classes{course.code}'))

            # Update courses data.
            course.credit = credit
            course.semester = semester
            course.save()

            # Instantiating course classes.
            for number in range(1, nb_classes + 1):
                capacity = random.randint(100, 500)
                models.CourseClass.objects.create(number=number, course=course, capacity=capacity)

        # Run algorithm.
        course_classes = models.CourseClass.objects.all()
        location_links = models.LocationLink.objects.all()

        engine = GAEngine(
            rooms=rooms,
            timeslots=timeslots,
            course_classes=course_classes,
            location_links=location_links,
            population_size=request.session['search_space'],
            num_generations=request.session['iterations']
        )
        solution, score, time_taken = engine.run()

        # Handle output.
        filename = 'timetable_' + str(round(time.time() * 1000))
        excel = Excel(filename=filename)
        excel.setup(rows=[t.code for t in timeslots], columns=[r.location.code + r.code for r in rooms])
        excel.write(solution=solution)

        result = {
            'algorithm': 'Genetic Algorithm',
            'conflict': score,
            'duration': time_taken,
            'domain': {
                'rooms': len(rooms),
                'classes': len(course_classes),
                'courses': request.session['nb_courses'],
                'timeslots': request.session['nb_timeslots'],
                'locations': request.session['nb_locations'],
                'travel_time': [f'{obj.location1}:{obj.location2}:{obj.travel_time}' for obj in location_links]
            }
        }

        yaml = Yaml(filename=filename)
        yaml.write(content=result)

        return render(request, 'views/congratulations.html', result)

    return render(request, 'views/step_3.html', context)

def restart(request):
    models.Location.objects.all().delete()
    models.Room.objects.all().delete()
    models.LocationLink.objects.all().delete()
    models.Course.objects.all().delete()
    models.CourseClass.objects.all().delete()
    models.Timeslot.objects.all().delete()
    return redirect('step_1')