from django.db import models
from django.contrib.auth.models import User
from .choices import SERVICES


# Create your models here.


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}/{self.city}/{self.phone}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
##########################################
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    qualification = models.TextField(null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE,null=True,blank=True)
    patients = models.ManyToManyField(Patient,null=True,blank=True) 
   
    

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"
########################################
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return f"{self.user.username}/{self.phone} / {self.clinic.name}"

class Apointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    service_type = models.CharField(max_length=100,choices=SERVICES)

    def __str__(self):
        return f"{self.patient.user.username}/{self.service_type}/{self.appointment_date}"
