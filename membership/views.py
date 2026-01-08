# membership/views.py
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Membership, Payment
from django.utils import timezone

PRICE_MAP = {
    '1M': Decimal('9.99'),
    '3M': Decimal('27.99'),
    '6M': Decimal('49.99'),
    '1Y': Decimal('89.99'),
}

@login_required
def create_membership(request):
    if request.method == 'POST':
        duration = request.POST.get('duration')
        if duration not in PRICE_MAP:
            messages.error(request, "Invalid selection.")
            return redirect('create_membership')
        request.session['membership_selection'] = {'duration': duration}
        return redirect('process_payment')

    context = {'price_map': {k: str(v) for k, v in PRICE_MAP.items()}}
    return render(request, 'membership/create.html', context)

@login_required
def membership_dashboard(request):
    membership = Membership.objects.filter(user=request.user).order_by('-start_date').first()
    return render(request, 'membership/dashboard.html', {'membership': membership})


@login_required
def process_payment(request):
    sel = request.session.get('membership_selection')
    if not sel:
        messages.info(request, "Please choose a membership plan first.")
        return redirect('create_membership')

    duration = sel.get('duration')
    if duration not in PRICE_MAP:
        messages.error(request, "Invalid membership plan selected.")
        return redirect('create_membership')

    amount = PRICE_MAP[duration]  # authoritative server-side price

    if request.method == 'POST':
        method = request.POST.get('method', 'Stripe')
        # Create membership and payment atomically
        # If you want transaction.atomic() you can wrap these in a transaction
        membership = Membership.objects.create(
            user=request.user,
            duration=duration,
        )
        Payment.objects.create(
            user=request.user,
            membership=membership,
            amount=amount,
            method=method,
            status='completed',
        )

        # Clear session selection and notify user
        request.session.pop('membership_selection', None)
        messages.success(request, "Payment confirmed. Your membership is now active.")
        return redirect('membership_dashboard')

    context = {
        'duration': duration,
        'amount': amount,
    }
    return render(request, 'membership/payment.html', context)

@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'membership/history.html', {'payments': payments})

