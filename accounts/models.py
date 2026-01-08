from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    height_feet = models.PositiveIntegerField(null=True, blank=True)
    height_inches = models.PositiveIntegerField(null=True, blank=True)
    weight_stone = models.PositiveIntegerField(null=True, blank=True)
    weight_pounds = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
