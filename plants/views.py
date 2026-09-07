from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Plant, CareLog
from .forms import PlantForm


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


@login_required
def plant_create(request):
    """ Add a new plant for the logged-in user. """
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            messages.success(
                request,
                f'{plant.nickname} has been added to your collection.',
            )
            return redirect(plant.get_absolute_url())
    else:
        form = PlantForm()

    return render(
        request,
        'plants/plant_form.html',
        {'form': form, 'is_edit': False},
    )


@login_required
def plant_update(request, pk):
    """ Edit an existing plant for the logged-in user. """
    plant = get_object_or_404(Plant, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'{plant.nickname} has been updated.',
            )
            return redirect(plant.get_absolute_url())
    else:
        form = PlantForm(instance=plant)

    return render(
        request,
        'plants/plant_form.html',
        {'form': form, 'is_edit': True},
    )


@login_required
def plant_delete(request, pk):
    """ Delete an existing plant for the logged-in user. """
    plant = get_object_or_404(Plant, pk=pk, user=request.user)

    if request.method == 'POST':
        nickname = plant.nickname
        plant.delete()
        messages.success(request, f'{nickname} has been deleted.')
        return redirect('plants:plant_list')

    return render(
        request,
        'plants/plant_confirm_delete.html',
        {'plant': plant},
    )
