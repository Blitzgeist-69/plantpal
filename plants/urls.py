from django.urls import path  # import path, similarr to project's urls.py
from . import views  # import views.py from the current directory

app_name = 'plants'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('plants/', views.plant_list, name='plant_list'),
]
