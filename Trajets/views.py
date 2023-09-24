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
        ville_arrive = trajet_filter.cleaned_data.get('arrivalCity')


        if date_depart and ville_depart and ville_arrive:
            trajets = trajets.filter(date_depart__gte=date_depart,lieu_depart=ville_depart,lieu_arrivee=ville_arrive)
            print(trajets)



    context = {'trajets': trajets, 'trajet_filter': trajet_filter,'VILLES_CHOICES':VILLES_CHOICES}
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
    print(trajets)

    return render(request, 'resultats_trajets_index.html', context)

import os
import folium
def Apropos(request):

    trajets = Trajet.objects.all()  # Utilisez 'objects' au lieu de 'objetcs'
    shp_dir = os.path.join(os.getcwd(), 'media', 'shp')
    # folium
    m = folium.Map(location=[-16.22, -71.59], zoom_start=10)
    ## style
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_rivers = {'color': 'blue'}
    ## adding to view

    folium.LayerControl().add_to(m)
    ## exporting
    m = m._repr_html_()
    context = {'my_map': m}

    return render(request, 'Apropos.html', context)

from geopy.geocoders import Nominatim



def details_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, pk=trajet_id)

    geolocator = Nominatim(user_agent="m.ryad@gmail.com")

    ville_depart = trajet.lieu_depart
    ville_arrivee = trajet.lieu_arrivee

    coord_depart = geolocator.geocode(ville_depart)
    coord_arrivee = geolocator.geocode(ville_arrivee)

    if coord_depart and coord_arrivee:
        latitude_depart = coord_depart.latitude
        longitude_depart = coord_depart.longitude
        latitude_arrivee = coord_arrivee.latitude
        longitude_arrivee = coord_arrivee.longitude

        print(f"Coordonnées de {ville_depart}: Latitude {latitude_depart}, Longitude {longitude_depart}")
        print(f"Coordonnées de {ville_arrivee}: Latitude {latitude_arrivee}, Longitude {longitude_arrivee}")
    else:
        print(f"Coordonnées introuvables pour {ville_depart} ou {ville_arrivee}")


    # Vous pouvez également gérer le formulaire de réservation ici
    context={'trajet': trajet ,'latitude_depart':latitude_depart,'longitude_depart':longitude_depart,
             'latitude_arrivee':latitude_arrivee,'longitude_arrivee':longitude_arrivee,}
    return render(request, 'details_trajet.html', context)