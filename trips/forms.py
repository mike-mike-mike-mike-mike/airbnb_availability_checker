from django import forms
from .models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["room_id", "check_in", "check_out"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }
