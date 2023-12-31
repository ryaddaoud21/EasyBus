from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Trajet ,Reservation ,Passager
from django.shortcuts import render,get_object_or_404
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
            context = {'trajets': trajets, 'trajet_filter': trajet_filter, 'VILLES_CHOICES': VILLES_CHOICES}
            return render(request, 'recherche_trajet.html', context)



    context = {'trajets': trajets, 'trajet_filter': trajet_filter,'VILLES_CHOICES':VILLES_CHOICES}
    return render(request, 'index.html', context)


def trajets(request):
    trajets = Trajet.objects.all()
    trajet_filter = TrajetFilterForm(request.GET)

    if trajet_filter.is_valid():
        date_min = trajet_filter.cleaned_data.get('date_min')
        ville_depart = trajet_filter.cleaned_data.get('departureCity')
        ville_arrivee = trajet_filter.cleaned_data.get('arrivalCity')


        if date_min and ville_depart and ville_arrivee:
            trajets = trajets.filter(date_depart__gte=date_min,lieu_depart=ville_depart,lieu_arrivee=ville_arrivee)
            print('hello')


    context = {'trajets': trajets, 'trajet_filter': trajet_filter, 'VILLES_CHOICES': VILLES_CHOICES}
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
from .models import VILLES_CHOICES
def Apropos(request):

    geolocator = Nominatim(user_agent="m.ryad@gmail.com")

    m = folium.Map(location=[36.7538, 3.0588], zoom_start=6)

    # Pour chaque ville, obtenez les coordonnées et ajoutez un marqueur à la carte
    for ville in VILLES_CHOICES:
        coord = geolocator.geocode(ville)
        if coord:
            latitude = coord.latitude
            longitude = coord.longitude
            folium.Marker([latitude, longitude], tooltip=ville).add_to(m)

    # Générez le code HTML de la carte
    map_html = m._repr_html_()

    return render(request, 'Apropos.html', {'map_html': map_html})

from geopy.geocoders import Nominatim
from barcode.writer import ImageWriter
from barcode import Code128
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.graphics.barcode import code128
from django.http import FileResponse, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.files import File

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




    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            trajet = Trajet.objects.get(id=trajet_id)
            passager = Passager(nom=form.cleaned_data['nom'],
                                prenom=form.cleaned_data['prenom'],
                                adresse_mail=form.cleaned_data['adresse_mail'],
                                numero_telephone=form.cleaned_data['numero_telephone'], )

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "dzd",
                            "unit_amount": int(trajet.prix)*100,
                            "product_data": {
                                "name": f"Payment de votre trajet de {trajet.lieu_depart} à {trajet.lieu_arrivee}",
                                },

                        },
                        "quantity": 1,
                    }
                ],
                metadata={"trajet_id": trajet.id ,"nom":form.cleaned_data['nom'] ,"prenom":form.cleaned_data['prenom'] ,
                          "adresse_mail":form.cleaned_data['adresse_mail'] ,"numero_telephone":form.cleaned_data['numero_telephone'] ,
                          "reservation_id":"" },
                mode="payment",
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
            print(checkout_session.metadata)
            return redirect(checkout_session.url)


        else:
            print (form.errors)


    # Vous pouvez également gérer le formulaire de réservation ici
    context={'trajet': trajet ,'latitude_depart':latitude_depart,'longitude_depart':longitude_depart,
             'latitude_arrivee':latitude_arrivee,'longitude_arrivee':longitude_arrivee}
    return render(request, 'details_trajet.html', context)





def reservation(request):
    form = ChercheReservation(request.GET or None)
    reservation = None
    if form.is_valid():
        numero_reservation = form.cleaned_data.get('numero_reservation')
        email_phone = form.cleaned_data.get('email_phone')

        try:
            reservation = Reservation.objects.get(id=numero_reservation,
                                                  passager__adresse_mail=email_phone)
            print(reservation)
            return render(request, 'details_reservation.html', {'reservation': reservation})


        except Reservation.DoesNotExist:
            print('pas de reservation')
            return render(request, 'details_reservation.html',{'reservation': reservation} )

        print(form.errors)
    return render(request, 'reservation.html', {'form': form, 'reservation': reservation})


from django.utils.http import urlquote

def details_reservation(request , reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.ticket:
        file_path = reservation.ticket.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = f'attachment; filename="{urlquote(reservation.ticket.name)}"'
        return response

    return render(request, 'details_reservation.html', { 'reservation': reservation})



from django.views import View


class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        trajet = Trajet.objects.get(id=self.kwargs["trajet_id"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                     "price_data": {
                        "currency": "usd",
                        "unit_amount": int(trajet.prix) ,
                        "product_data": {
                            "name": trajet.lieu_depart,
                            "description": trajet.lieu_arrivee,

                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"trajet_id": trajet.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)




from django.views.generic import TemplateView






class CancelView(TemplateView):
    template_name = "Cancel.html"

from django.core.mail import EmailMessage
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.mail import send_mail # Add this
from .models import PaymentHistory # Add this
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.cache import cache
from django.contrib.sessions.models import Session
import  qrcode
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):

    def post(self, request, format=None,):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)


        if event["type"] == "checkout.session.completed":
            print("Payment successful")

            # Add this
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            trajet_id = session["metadata"]["trajet_id"]
            nom = session["metadata"]["nom"]
            adresse_mail = session["metadata"]["adresse_mail"]
            prenom = session["metadata"]["prenom"]
            numero_telephone = session["metadata"]["numero_telephone"]
            trajet = get_object_or_404(Trajet, id=trajet_id)
            print(nom,prenom,adresse_mail,numero_telephone)
            passager = Passager(nom=nom,
                                prenom=prenom,
                                adresse_mail=adresse_mail,
                                numero_telephone=numero_telephone )
            passager.save()
            print(passager)
            reservation = Reservation(
                passager=passager,
                trajet=trajet,
                methodePaiement="carte_credit",
                nombre_passagers=1,
            )
            reservation.save()
            session["metadata"]["reservation_id"] = reservation.id
            reservation_id=session["metadata"]["reservation_id"]
            print(reservation_id)
            print(reservation)




            PaymentHistory.objects.create(
                email=customer_email, trajet=trajet, payment_status="completed"
            )
            numero_reservation=str(reservation.id)

            code = Code128(numero_reservation, writer=ImageWriter())
            nom_fichier = f'Barcode/{numero_reservation}'

            # Assurez-vous que le dossier 'Barcode' existe (créez-le s'il n'existe pas)
            dossier_barcode = os.path.dirname(nom_fichier)
            os.makedirs(dossier_barcode, exist_ok=True)

            # Enregistrez le code-barres en tant qu'image dans le dossier spécifié
            code.save(nom_fichier)



            # Générez le numéro de réservation (à remplacer par le vrai numéro)
            numero_reservation = str(reservation.id)


            # Définissez le chemin du fichier PDF
            pdf_file_path = f'PDFs/ticket_{numero_reservation}.pdf'


            # Créez un document PDF
            doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)

            # Créez une liste d'éléments pour le PDF
            elements = []

            # Ajoutez le titre du ticket
            title_style = ParagraphStyle(name='TitleStyle', fontSize=20, alignment=1)
            title = Paragraph("Ticket de Réservation", title_style)
            elements.append(title)

            # Ajoutez un espace entre le titre et les détails
            elements.append(Spacer(1, 24))

            # Ajoutez les détails de réservation
            details_style = ParagraphStyle(name='DetailsStyle', fontSize=12, textColor=colors.black)
            details_reservation = [
                f"<b>Numéro de réservation :</b> {numero_reservation}",
                f"<b>Nom :</b> {reservation.passager.nom}",
                f"<b>Prénom :</b> {reservation.passager.prenom}",
                f"<b>Adresse e-mail :</b> {reservation.passager.adresse_mail}",
                f"<b>Numéro de téléphone :</b> {reservation.passager.numero_telephone}",
                f"<b>Lieu de départ :</b> {reservation.trajet.lieu_depart}",
                f"<b>Lieu d'arrivée :</b> {reservation.trajet.lieu_arrivee}",
                f"<b>Date de départ :</b> {reservation.trajet.date_depart}",
                f"<b>Date d'arrivée :</b> {reservation.trajet.date_arrivee}",
                f"<b>Date de réservation :</b> {reservation.date_reservation}",
                f"<b>Prix :</b> {reservation.trajet.prix} DA",
            ]

            for detail in details_reservation:
                detail_paragraph = Paragraph(detail, details_style)
                elements.append(detail_paragraph)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(numero_reservation)
            qr.make(fit=True)

            # Créez une image à partir du code QR généré
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image_file = f'QRCode/qrcode_{numero_reservation}.png'
            qr_image.save(qr_image_file)
            qr_directory = 'QRCode/'

            qr_file_path = os.path.join(qr_directory, f'qrcode_{numero_reservation}.png')
            qr_image.save(qr_file_path)

            # ...

            # Ajoutez l'image du code QR au PDF
            elements.append(Image(qr_image_file, width=100, height=100))

            # Construisez le PDF en ajoutant les éléments
            doc.build(elements)

            # Associez le chemin du fichier PDF à la réservation
            reservation.ticket = pdf_file_path
            reservation.save()

            reservation_id =reservation.id

            numero_reservation = str(reservation.id)



            with open(pdf_file_path, 'rb') as pdf_file:
                reservation.ticket.save(f'ticket_{numero_reservation}.pdf', File(pdf_file), save=True)
            reservation_id = reservation.id
            # Redirigez l'utilisateur vers la page de succès

            email = EmailMessage(
                subject=f"Votre Nouvelle Réservation :{reservation_id}",
                body=f"Votre réservation est confirmée , Merci d’avoir choisi de voyager avec nous ! Vous trouverez ci-dessous un bref aperçu de votre/vos prochain(s) trajet(s) :{trajet.lieu_depart} à {trajet.lieu_arrivee}",
                from_email="m.ryaddaod21@gmail.com",
                to=[customer_email],
            )

            # Joignez le fichier PDF en tant que pièce jointe
            email.attach_file(pdf_file_path, 'application/pdf')

            # Envoyez l'e-mail
            email.send()




        return HttpResponse(status=200)


def Success(request):
    try:
        latest_reservation = Reservation.objects.latest('id')
    except Reservation.DoesNotExist:
        latest_reservation = None
    print(latest_reservation)

    # Renvoyez une réponse HTTP avec le contenu HTML rendu à partir du modèle
    return render(request, 'success.html',{'reservation': latest_reservation})

