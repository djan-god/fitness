from django.db import models
from django.conf import settings
from datetime import timedelta, date
from django.utils import timezone

class Membership(models.Model):
    DURATION_CHOICES = [
        ('1M', '1 Month'),
        ('3M', '3 Months'),
        ('6M', '6 Months'),
        ('1Y', '1 Year'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    

    def save(self, *args, **kwargs):
        # Ensure start_date exists (auto_now_add may not be set on the instance before first save)
        if not self.start_date:
            self.start_date = timezone.localdate()
        durations = {'1M': 30, '3M': 90, '6M': 180, '1Y': 365}
        days = durations.get(self.duration, 30)
        self.end_date = self.start_date + timedelta(days=days)
        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=20)  # e.g., 'Stripe', 'PayPal'
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='completed')


    def __str__(self):
        return f"{self.user} - £{self.amount} on {self.date.strftime('%Y-%m-%d')} ({self.method})"
