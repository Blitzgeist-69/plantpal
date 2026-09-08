from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Plant
from .forms import PlantForm, CareLogForm
from django.utils import timezone


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
    """ Split user's plants into due/overdue and up to date based
    on watering schedule.
    """
    plants = Plant.objects.filter(
        user=request.user,
    ).prefetch_related('care_logs')

    needs_attention = []
    doing_fine = []
    for plant in plants:
        if plant.needs_attention():
            needs_attention.append(plant)
        else:
            doing_fine.append(plant)

    context = {
        'needs_attention': needs_attention,
        'doing_fine': doing_fine,
    }
    return render(request, 'plants/dashboard.html', context)


@login_required
def plant_list(request):
    """List of plants for the logged-in user."""
    plants = Plant.objects.filter(user=request.user).order_by('nickname')
    return render(request, 'plants/plant_list.html', {'plants': plants})


@login_required
def plant_detail(request, pk):
    """
    Detail view for a plant belonging to a user. If the plant does not
    belong to the user, return a 404 error. Show care history and accept a
    new carelog.
    """
    plant = get_object_or_404(Plant, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CareLogForm(request.POST)
        if form.is_valid():
            care_log = form.save(commit=False)
            care_log.plant = plant
            care_log.save()
            messages.success(
                request,
                f'Logged {care_log.get_action_display()} for '
                f'{plant.nickname}.',
            )
            return redirect(plant.get_absolute_url())
    else:
        form = CareLogForm(initial={'date': timezone.localdate()})

    care_logs = plant.care_logs.all()
    context = {'plant': plant, 'care_logs': care_logs, 'care_form': form}
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
