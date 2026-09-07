from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Plant, CareLog


def home(request):
    """Public landing page. Logged-in users go to the dashboard."""
    if request.user.is_authenticated:
        return redirect('plants:dashboard')
    return render(request, 'home.html')


def register(request):
    """Create an account, then log the new user in."""
    if request.user.is_authenticated:
        return redirect('plants:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to PlantPal.')
            return redirect('plants:dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """Logged-in home. Plant lists will be added later."""
    return render(request, 'plants/dashboard.html')


@login_required
def plant_list(request):
    """List of plants for the logged-in user."""
    plants = Plant.objects.filter(user=request.user).order_by('nickname')
    return render(request, 'plants/plant_list.html', {'plants': plants})


@login_required
def plant_detail(request, pk):
    """
    Detail view for a plant belonging to a user. If the plant does not
    belong to the user, return a 404 error.
    """
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    care_logs = plant.care_logs.all()
    context = {'plant': plant, 'care_logs': care_logs}
    return render(request, 'plants/plant_detail.html', context)
