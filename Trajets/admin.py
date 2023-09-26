from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(Trajet)
admin.site.register(Passager)
admin.site.register(Reservation)
admin.site.register(PaymentHistory)