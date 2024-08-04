from django.shortcuts import render, redirect
from utils.serializer import ModelToDictSerializer
from . import service, models

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
        request.session['travel_time_dict'] = {f'travel_time_{i}_{j}': request.POST[f'travel_time_{i}_{j}']
                                               for i in range(1, int(request.session['nb_locations']))
                                               for j in range(i + 1, int(request.session['nb_locations']) + 1)}
        return redirect('step_3')
        
    return render(request, 'views/step_2.html', context)

def step_3(request):
    generator = service.DataGeneratorService(
        rooms_dict=request.session['rooms_dict'],
        nb_courses=request.session['nb_courses'],
        nb_timeslots=request.session['nb_timeslots'],
        nb_locations=request.session['nb_locations'],
    )

    request.session['rooms'] = ModelToDictSerializer.serialize_many(generator.get_rooms())
    request.session['courses'] = ModelToDictSerializer.serialize_many(generator.get_courses())
    request.session['locations'] = ModelToDictSerializer.serialize_many(generator.get_locations())
    request.session['timeslots'] = ModelToDictSerializer.serialize_many(generator.get_timeslots())

    context = {
        'courses': ModelToDictSerializer.deserialize_many(models.Course, request.session['courses'])
    }

    if request.method == 'POST':
        # TODO 1 Update courses data.
        # TODO 2 Instantiating course classes.
        # TODO 2 Run algorithm.
        # TODO 3 Handle output.
        pass

    return render(request, 'views/step_3.html', context)