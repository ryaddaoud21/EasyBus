from django.shortcuts import render
from django.urls import path
from .views import *

# Create your views here.


urlpatterns = [
    path('', index , name='index'),
    path('trajets/',trajets,name='liste_trajets'),
    path('Recherche_trajets/',rechercher_trajets,name='rechercher_trajets'),
    path('Apropos/', Apropos, name='Apropos'),
    path('reservation/', reservation, name='reservation'),
    path('rechercher_trajets_index/', rechercher_trajets_index, name='rechercher_trajets_index'),
    path('trajets/<int:trajet_id>/', details_trajet, name='details_trajet'),
    path('reservation/<int:reservation_id>/', details_reservation, name='details_reservation'),


    path( "checkout/<int:trajet_id>/", CreateStripeCheckoutSessionView.as_view(),  name="checkout" ),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),

]
