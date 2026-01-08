from django import forms
from .models import WeightEntry, Goal
from accounts.models import CustomUser

class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['stones', 'pounds']

    def clean_pounds(self):
        pounds = self.cleaned_data.get('pounds')
        if pounds is None:
            return pounds
        if pounds >= 14:
            raise forms.ValidationError("Pounds must be less than 14")
        return pounds


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['target_stones', 'target_pounds']


class HeightForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['height_feet', 'height_inches']
