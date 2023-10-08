from django.db import models
from django.urls import reverse

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

class Trajet(models.Model):
    id = models.AutoField(primary_key=True)
    lieu_depart = models.CharField(max_length=100, choices=VILLES_CHOICES)
    lieu_arrivee = models.CharField(max_length=100, choices=VILLES_CHOICES)
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    prix = models.DecimalField(max_digits=10, decimal_places=2,default=10)

    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return f"{self.lieu_depart} - {self.lieu_arrivee}"

    @property
    def duree_trajet(self):
        # Calcul de la durée en soustrayant date_depart de date_arrivee
        duree = self.date_arrivee - self.date_depart

        # La durée est maintenant stockée dans un objet timedelta
        # Vous pouvez extraire les jours, les heures, les minutes, etc. si nécessaire
        return duree

    def duree_minutes(self):
        return int(self.duree_trajet.total_seconds() / 60)

    def duree_formattee(self):
        heures, minutes = divmod(self.duree_minutes(), 60)
        return f"{heures:02d}H:{minutes:02d}min"


    def __str__(self):
        return f"Trajet de {self.lieu_depart} à {self.lieu_arrivee}"


class Passager(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse_mail = models.EmailField(default='adresse_par_defaut@example.com')
    numero_telephone = models.CharField(max_length=20, default='0780342309')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    # Ajoutez d'autres champs selon vos besoins

class Reservation(models.Model):
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE,null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    nombre_passagers = models.PositiveIntegerField(default=1)
    METHODES_PAIEMENT = [
        ('carte_credit', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('virement', 'Virement bancaire'),
    ]
    methodePaiement = models.CharField(max_length=20, choices=METHODES_PAIEMENT,default='carte_credit')
    ticket = models.FileField(upload_to='tickets/', null=True, blank=True)

    def get_ticket_url(self):
        if self.ticket:
            return reverse('details_reservation', kwargs={'reservation_id': self.id})
        return None


    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return f"Réservation {self.id} ({self.trajet})"



class PaymentHistory(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, ("pending")),
        (COMPLETED, ("completed")),
        (FAILED, ("failed")),   )

    email = models.EmailField()  # Supprimez unique=True
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE,null=True)
    payment_status = models.CharField(  max_length=1, choices=STATUS_CHOICES, default=PENDING )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.trajet)





