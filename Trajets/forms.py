from django import forms
from .models import VILLES_CHOICES


class ChercherTrajet(forms.Form):

    departureDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    departureCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)
    arrivalCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)

class TrajetFilterForm(forms.Form):
    date_min = forms.DateField(label="Date minimale", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
