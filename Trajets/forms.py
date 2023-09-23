from django import forms
from .models import VILLES_CHOICES

class TrajetForm(forms.Form):
    TRIP_CHOICES = [('allerSimple', 'Aller Simple'), ('allerRetour', 'Aller-Retour')]

    trip_type = forms.ChoiceField(choices=TRIP_CHOICES, widget=forms.RadioSelect)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'disabled': 'disabled'}))
    # Autres champs de formulaire, par exemple, les lieux de départ et d'arrivée, le nombre de passagers, etc.


class ChercherTrajet(forms.Form):

    departureDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    departureCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)
    arrivalCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)

class TrajetFilterForm(forms.Form):
    date_min = forms.DateField(label="Date minimale", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
