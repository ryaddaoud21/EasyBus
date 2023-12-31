# Generated by Django 3.2.17 on 2023-09-25 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passager',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('adresse_mail', models.EmailField(default='adresse_par_defaut@example.com', max_length=254)),
                ('numero_telephone', models.CharField(default='0780342309', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu_depart', models.CharField(choices=[('Alger', 'Alger'), ('Oran', 'Oran'), ('Constantine', 'Constantine'), ('Annaba', 'Annaba'), ('Tlemcen', 'Tlemcen'), ('Tizi Ouzou', 'Tizi Ouzou'), ('Béjaïa', 'Béjaïa'), ('Blida', 'Blida'), ('Sétif', 'Sétif'), ('Biskra', 'Biskra')], max_length=100)),
                ('lieu_arrivee', models.CharField(choices=[('Alger', 'Alger'), ('Oran', 'Oran'), ('Constantine', 'Constantine'), ('Annaba', 'Annaba'), ('Tlemcen', 'Tlemcen'), ('Tizi Ouzou', 'Tizi Ouzou'), ('Béjaïa', 'Béjaïa'), ('Blida', 'Blida'), ('Sétif', 'Sétif'), ('Biskra', 'Biskra')], max_length=100)),
                ('date_depart', models.DateTimeField()),
                ('date_arrivee', models.DateTimeField()),
                ('prix', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('nombre_passagers', models.PositiveIntegerField(default=1)),
                ('methodePaiement', models.CharField(choices=[('carte_credit', 'Carte de crédit'), ('paypal', 'PayPal'), ('virement', 'Virement bancaire')], default='carte_credit', max_length=20)),
                ('passager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trajets.passager')),
                ('trajet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trajets.trajet')),
            ],
        ),
    ]
