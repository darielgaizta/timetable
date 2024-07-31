from django.shortcuts import render, redirect

# Create your views here.
def step_1(request):
    if request.method == 'POST':
        return redirect(step_2)
    return render(request, 'views/step_1.html')

def step_2(request):
    if request.method == 'POST':
        if request.POST.get('previous', 0): return redirect(step_1)
    return render(request, 'views/step_2.html')