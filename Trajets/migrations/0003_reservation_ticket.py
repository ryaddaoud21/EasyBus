# Generated by Django 3.2.17 on 2023-09-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trajets', '0002_alter_trajet_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='ticket',
            field=models.FileField(blank=True, null=True, upload_to='tickets/'),
        ),
    ]
