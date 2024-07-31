from django.urls import path
from . import views

urlpatterns = [
    path('1/', views.step_1, name='step_1'),
    path('2/', views.step_2, name='step_2'),
]
