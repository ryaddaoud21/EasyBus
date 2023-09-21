from django.db import models

from django.contrib.auth.models import User
from django.db import models

from django.db import models

class Trajet(models.Model):
        VILLES_CHOICES = [
            ('Alger', 'Alger'),
            ('Oran', 'Oran'),
            ('Constantine', 'Constantine'),
            ('Annaba', 'Annaba'),
            ('Tlemcen', 'Tlemcen'),
            ('Tizi Ouzou', 'Tizi Ouzou'),
            ('Béjaïa', 'Béjaïa'),
            ('Blida', 'Blida'),
            ('Sétif', 'Sétif'),
            ('Biskra', 'Biskra'),
        ]

        lieu_depart = models.CharField(max_length=100, choices=VILLES_CHOICES)
        lieu_arrivee = models.CharField(max_length=100, choices=VILLES_CHOICES)
        date_depart = models.DateTimeField()
        date_arrivee = models.DateTimeField()
        prix = models.DecimalField(max_digits=10, decimal_places=2,default=10)

        # Ajoutez d'autres champs selon vos besoins

        def __str__(self):
            return f"{self.lieu_depart} - {self.lieu_arrivee}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liaison avec le modèle User
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    nombre_passagers = models.PositiveIntegerField()
    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return f"Réservation {self.id} ({self.trajet})"

class Passager(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return f"{self.prenom} {self.nom}"
