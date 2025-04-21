from django.contrib import admin
from .models import Clinic,Patient,Doctor,Nurse,Apointment

admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Apointment)


# Register your models here.
