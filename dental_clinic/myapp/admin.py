from django.contrib import admin
from .models import Clinic,Patient,Doctor,Nurse,Apointment
from rest_framework.authtoken.models import Token
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Apointment)


# Register your models here.
