from django.shortcuts import render
from django.urls import path
from .views import *

# Create your views here.


urlpatterns = [
    path('', index , name='index'),
    path('trajets/',trajets,name='liste_trajets'),
    path('rechercher_trajets/', rechercher_trajets, name='rechercher_trajets'),

]
