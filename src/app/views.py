from django.shortcuts import render, redirect

# Create your views here.
def step_1(request):
    if request.method == 'POST':
        request.session['nb_courses'] = request.POST['courses']
        request.session['nb_timeslots'] = request.POST['timeslots']
        request.session['nb_locations'] = request.POST['locations']
        return redirect('step_2')
    
    return render(request, 'views/step_1.html')

def step_2(request):
    context = {
        'nb_courses': range(1, int(request.session['nb_courses']) + 1),
        'nb_timeslots': range(1, int(request.session['nb_timeslots']) + 1),
        'nb_locations': range(1, int(request.session['nb_locations']) + 1),
    }
    
    if request.method == 'POST':
        request.session['search_space'] = request.POST['search_space']
        request.session['iterations'] = request.POST['iterations']
        request.session['rooms_dict'] = {f'rooms{i}': request.POST[f'rooms{i}'] for i in context['nb_locations']}
        request.session['travel_time_dict'] = {f'travel_time_{i}_{j}': request.POST[f'travel_time_{i}_{j}']
                                               for i in range(1, int(request.session['nb_locations']))
                                               for j in range(i + 1, int(request.session['nb_locations']) + 1)}
        return redirect('step_3')        
        
    return render(request, 'views/step_2.html', context)

def step_3(request):
    context = {}

    if request.method == 'POST':
        pass
        
        # TODO 1 Instantiate data.
        # TODO 2 Run algorithm.
        # TODO 3 Handle output.

    return render(request, 'views/step_3.html', context)