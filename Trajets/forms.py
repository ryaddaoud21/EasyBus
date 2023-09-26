import stripe as stripe
from django import forms
from .models import VILLES_CHOICES


class ChercherTrajet(forms.Form):

    departureDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    departureCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)
    arrivalCity = forms.ChoiceField(choices=VILLES_CHOICES, required=False)

class TrajetFilterForm(forms.Form):
    date_min = forms.DateField(label="Date minimale", required=False, widget=forms.DateInput(attrs={'type': 'date'}))


from django import forms


class ReservationForm(forms.Form):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    adresse_mail = forms.EmailField()
    numero_telephone = forms.CharField(max_length=20)

    METHODES_PAIEMENT = [
        ('carte_credit', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('virement', 'Virement bancaire'),
    ]
    methode_paiement = forms.ChoiceField(choices=METHODES_PAIEMENT)


class ChercheReservation(forms.Form):
    numero_reservation = forms.CharField(label="N° de réservation", max_length=100, required=True)
    email_phone = forms.CharField(label="E-Mail ou numéro de téléphone", max_length=100, required=True)


from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    exp_month = forms.CharField(label='Expiry Month', widget=forms.TextInput(attrs={'placeholder': 'MM'}))
    exp_year = forms.CharField(label='Expiry Year', widget=forms.TextInput(attrs={'placeholder': 'YYYY'}))
    cvc = forms.CharField(label='CVC', widget=forms.TextInput(attrs={'placeholder': 'CVC'}))

    def process_payment(self, amount):
        token = self.cleaned_data.get('stripeToken')
        print(token)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
            )
            return True
        except stripe.error.CardError as e:
            # Handle card error (e.g., card declined)
            return str(e)
        except Exception as e:
            # Handle other errors
            return str(e)
