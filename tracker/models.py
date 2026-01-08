from django.db import models
from django.conf import settings

def stones_pounds_to_kg(stones: int, pounds: int) -> float:
    total_pounds = stones * 14 + pounds
    return round(total_pounds * 0.45359237, 2)

class Goal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goal')
    target_stones = models.PositiveIntegerField()
    target_pounds = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def target_kg(self) -> float:
        return stones_pounds_to_kg(self.target_stones, self.target_pounds)


class WeightEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weights')
    stones = models.PositiveIntegerField(default=0)
    pounds = models.PositiveIntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    @property
    def kg(self) -> float:
        return stones_pounds_to_kg(self.stones, self.pounds)

    @property
    def bmi(self) -> float | None:
        user = self.user
        if not user.height_feet and not user.height_inches:
            return None
        total_inches = (user.height_feet or 0) * 12 + (user.height_inches or 0)
        if total_inches <= 0:
            return None
        meters = total_inches * 0.0254
        return round(self.kg / (meters * meters), 1)

    @property
    def age_at_record(self) -> int | None:
        dob = self.user.date_of_birth
        if not dob:
            return None
        rec_date = self.recorded_at.date()
        years = rec_date.year - dob.year - ((rec_date.month, rec_date.day) < (dob.month, dob.day))
        return years
