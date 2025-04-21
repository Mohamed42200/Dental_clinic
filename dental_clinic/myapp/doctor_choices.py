from rest_framework.response import Response
from . models import Doctor

def doctor_choices(request):
    doctors = Doctor.objects.all()
    choices = [
        {'name': doctor.user.username}
        for doctor in doctors
    ]
    return Response(choices)

