from django.urls import path  # import path, similarr to project's urls.py
from . import views  # import views.py from the current directory

app_name = 'plants'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('plants/', views.plant_list, name='plant_list'),
    path('plants/add/', views.plant_create, name='plant_create'),
    path('plants/<int:pk>/edit/', views.plant_update, name='plant_update'),
    path('plants/<int:pk>/delete/', views.plant_delete, name='plant_delete'),
    path('plants/<int:pk>/', views.plant_detail, name='plant_detail'),
]
