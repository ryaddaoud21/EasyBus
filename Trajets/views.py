from django.shortcuts import render,redirect,reverse
from .models import Trajet

# Create your views here.
from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        lieu_depart = request.POST.get('departure')
        lieu_arrivee = request.POST.get('arrival')
        date_depart = request.POST.get('departureDate')
        date_arrivee = request.POST.get('arrivalDate')
        nombre_passagers = request.POST.get('passengers')

        # Vous pouvez maintenant effectuer une recherche de trajets en utilisant les données saisies
        # par l'utilisateur. Par exemple :
        trajets = Trajet.objects.filter(ville_depart=lieu_depart, ville_arrivee=lieu_arrivee,
                                        date_depart=date_depart, date_arrivee=date_arrivee)

        # Vérifiez si des trajets ont été trouvés
        if trajets.exists():
            # Si des trajets ont été trouvés, envoyez-les à un modèle pour les afficher
            return render(request, 'resultats_trajets.html', {'trajets': trajets})
        else:
            # Si aucun trajet n'a été trouvé, redirigez vers une page indiquant qu'il n'y a pas de trajet pour cette date
            return render(request, 'pas_de_trajet.html')

    return render(request, 'index.html')


def trajets(request):

    trajets = Trajet.objects.all()  # Utilisez 'objects' au lieu de 'objetcs'
    context = {'trajets': trajets}
    return render(request, 'trajet.html', context)


def rechercher_trajets(request):

    trajets = Trajet.objects.all()  # Utilisez 'objects' au lieu de 'objetcs'
    context = {'trajets': trajets}

    return render(request, 'resultats_trajets.html', context)