from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import WeightEntryForm, GoalForm, HeightForm
from .models import WeightEntry, Goal

@login_required
def tracker_dashboard(request):
    user = request.user
    goal_instance = getattr(user, 'goal', None)

    gform = GoalForm(instance=goal_instance)
    wform = WeightEntryForm()
    hform = HeightForm(instance=user)

    if request.method == 'POST':
        if 'save_weight' in request.POST:
            wform = WeightEntryForm(request.POST)
            if wform.is_valid():
                entry = wform.save(commit=False)
                entry.user = user
                entry.save()
                return redirect('tracker:dashboard')

        elif 'save_goal' in request.POST:
            gform = GoalForm(request.POST, instance=goal_instance)
            if gform.is_valid():
                obj = gform.save(commit=False)
                obj.user = user
                obj.save()
                return redirect('tracker:dashboard')

        elif 'save_height' in request.POST:
            hform = HeightForm(request.POST, instance=user)
            if hform.is_valid():
                hform.save()
                return redirect('tracker:dashboard')

    weights = user.weights.order_by('-recorded_at')
    latest = weights.first()

    dob = user.date_of_birth
    age_now = None
    is_child = False
    if dob:
        today = timezone.now().date()
        age_now = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        is_child = age_now < 18

    distance_kg = None
    if latest and goal_instance:
        distance_kg = round(abs(latest.kg - goal_instance.target_kg), 2)

    chart_dates = [e.recorded_at.strftime('%Y-%m-%d') for e in weights[::-1]]
    chart_bmis = [e.bmi if e.bmi is not None else None for e in weights[::-1]]

    context = {
        'wform': wform,
        'gform': gform,
        'hform': hform,
        'latest': latest,
        'goal': goal_instance,
        'distance_kg': distance_kg,
        'weights': weights,
        'age_now': age_now,
        'is_child': is_child,
        'chart_dates': chart_dates,
        'chart_bmis': chart_bmis,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def history_view(request):
    weights = request.user.weights.order_by('-recorded_at')
    return render(request, 'tracker/history.html', {'weights': weights})
