from django.shortcuts import render,redirect,reverse
from .models import Trajet

# Create your views here.
from django.shortcuts import render,get_object_or_404
from .models import VILLES_CHOICES
from .forms import *
def index(request):
    trajets = Trajet.objects.all()
    trajet_filter = ChercherTrajet(request.GET)

    if trajet_filter.is_valid():
        date_depart = trajet_filter.cleaned_data.get('departureDate')
        ville_depart = trajet_filter.cleaned_data.get('departureCity')
        ville_arrivee = trajet_filter.cleaned_data.get('arrivalCity')

        if date_depart:
            trajets = trajets.filter(date_depart=date_depart)

        if ville_depart:
            trajets = trajets.filter(lieu_depart=ville_depart)

        if ville_arrivee:
            trajets = trajets.filter(lieu_arrivee=ville_arrivee)

    context = {'trajets_index': trajets, 'trajet_filter': trajet_filter}
    return render(request, 'index.html', context)


def trajets(request):
    trajets = Trajet.objects.all()
    trajet_filter = TrajetFilterForm(request.GET)

    if trajet_filter.is_valid():
        date_min = trajet_filter.cleaned_data.get('date_min')

        if date_min:
            trajets = trajets.filter(date_depart__gte=date_min)


    context = {'trajets': trajets, 'trajet_filter': trajet_filter}
    return render(request, 'trajet.html', context)


def rechercher_trajets(request):

    trajets = Trajet.objects.all()  # Utilisez 'objects' au lieu de 'objetcs'
    context = {'trajets': trajets}

    return render(request, 'resultats_trajets.html', context)

def rechercher_trajets_index(request):

    trajets = Trajet.objects.all()  # Utilisez 'objects' au lieu de 'objetcs'
    context = {'trajets': trajets}

    return render(request, 'resultats_trajets_index.html', context)



def details_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, pk=trajet_id)

    # Vous pouvez également gérer le formulaire de réservation ici

    return render(request, 'details_trajet.html', {'trajet': trajet})