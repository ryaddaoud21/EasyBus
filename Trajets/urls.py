from django.shortcuts import render
from django.urls import path
from .views import *

# Create your views here.


urlpatterns = [
    path('', index , name='index'),
    path('trajets/',trajets,name='liste_trajets'),
    path('Apropos/', Apropos, name='Apropos'),

    path('rechercher_trajets/', rechercher_trajets, name='rechercher_trajets'),
    path('rechercher_trajets_index/', rechercher_trajets_index, name='rechercher_trajets_index'),

    path('trajets/<int:trajet_id>/', details_trajet, name='details_trajet'),

]
