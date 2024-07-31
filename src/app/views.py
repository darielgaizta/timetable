from django.shortcuts import render, redirect

# Create your views here.
def step_1(request, context={}):
    if request.method == 'POST':
        return redirect(step_2)
    return render(request, 'views/step_1.html', context)

def step_2(request, context={}):
    if request.method == 'POST':
        if request.POST.get('previous', 0): return redirect(step_1)
        if request.POST.get('next', 0):
            # TODO Process data
            return redirect(step_3)
    return render(request, 'views/step_2.html', context)

def step_3(request, context={}):
    if request.method == 'POST':
        if request.POST.get('previous', 0): return redirect(step_2)
    return render(request, 'views/step_3.html', context)