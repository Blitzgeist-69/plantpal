from django.urls import path  # import path, similarr to project's urls.py
from . import views  # import views.py from the current directory

urlpatterns = [
    path('', views.index, name='index'),  # define a URL pattern for the index view
]
