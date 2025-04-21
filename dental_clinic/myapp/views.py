from django.shortcuts import render,get_list_or_404
from django.db import transaction
from django.contrib.auth.models import User
#rest_framework
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#serializers
from .serializers import Create_Doctor_Serializer,UserSerializer
from . serializers import Create_Clinic_Serializer
from .serializers import Create_Nurse_Serializer
from .serializers import create_patient_serializer
from .serializers import Appointment_Serializer

#models
from .models import Doctor,Clinic,Nurse,Patient,Apointment


# Create your views here.
@api_view(['GET'])
def doctors(request):

    doctors =User.objects.filter(doctor__isnull = False)

    return Response(doctors.values('username'))


@api_view(['POST'])
def create_new_patient(request):

    try:
        serializer = create_patient_serializer(data = request.data)

        if serializer.is_valid():
            user_data = serializer.validated_data['user']
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']

            photo = serializer.validated_data['photo']
            phone=  serializer.validated_data['phone']
            address = serializer.validated_data['address']
            clinic_name = serializer.validated_data['clinic_name']

            clinic = Clinic.objects.filter(name =clinic_name ).first()
            if not clinic:
                return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)



            with transaction.atomic():
                user = User.objects.create(
                    username = username,
                    email = email,
                    password = password
                )
                patient = Patient.objects.create(
                    user = user,
                    photo = photo,
                    phone = phone,
                    address = address, 
                    clinic = clinic
                )
                return Response({'message':'created successfully'},status=status.HTTP_201_CREATED)
        return Response({'Error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({'m/Ex':str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_doctor(request):

    try:
        serializer =Create_Doctor_Serializer(data = request.data)
        if serializer.is_valid():
             user_data = serializer.validated_data['user']
             username = user_data['username']
             email = user_data['email']
             password = user_data['password']

             phone = serializer.validated_data['phone']
             specialization = serializer.validated_data['specialization']
             qualification = serializer.validated_data['qualification'] 

             clinic_name = serializer.validated_data['clinic_name']


             clinic = Clinic.objects.filter(name = clinic_name).first()
             if not clinic:
                    return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)

# ⛑️ Rollback block starts here
             with transaction.atomic():
                 user =  User.objects.create_user(
                     username =username,
                     email=email,
                     password=password,
                     )
                 doctor = Doctor.objects.create(
                      user = user,
                      phone = phone,
                      specialization = specialization,
                      qualification = qualification,
                      clinic = clinic
                      )
                 return Response({'message':'created successfully'},status=status.HTTP_201_CREATED)
             
        return Response({'Error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            

    except Exception as e:
        return Response({'m':str(e)},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_new_nurse(request):

    try:
        serializer = Create_Nurse_Serializer(data = request.data)  
        if serializer.is_valid():
            user_data = serializer.validated_data['user']

            username = user_data['username']
            email = user_data['email']
            password = user_data['password']

            phone = serializer.validated_data['phone']
            clinic_name = serializer.validated_data['clinic_name']

            clinic = Clinic.objects.filter(name = clinic_name).first()
            if not clinic:
                return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)


            with transaction.atomic():

                user = User.objects.create(
                    username = username,
                    email = email,
                    password = password
                )

                nurse = Nurse.objects.create(
                    user = user,
                    phone = phone,
                    clinic = clinic
                )
                return Response({'message':'created successfully'},status=status.HTTP_201_CREATED)
        return Response({'Error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'m':str(e)},status=status.HTTP_400_BAD_REQUEST)


    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_clinic(request):
    try:
        serializer = Create_Clinic_Serializer(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            address = serializer.validated_data['address']
            phone =serializer.validated_data['phone']
            city = serializer.validated_data['city']
            
            with transaction.atomic():

                clinic = Clinic.objects.create(
                name = name,
                address = address,
                phone = phone,
                city = city
            )
            return Response({'message': f"clinic : {name} created successfully"}, status=status.HTTP_201_CREATED)
        return Response({'Error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
    except ValidationError as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    try:
      
        serializer = Appointment_Serializer(data = request.data)

        if serializer.is_valid():

            appointment_date = serializer.validated_data['appointment_date']
            service_type = serializer.validated_data['service_type']
            try:
                patient = Patient.objects.get(user=request.user)
            except Patient.DoesNotExist:
                return Response({'error': 'This user is not a patient.'}, status=404)

            with transaction.atomic():

                appointment = Apointment.objects.create(
                    patient = patient,
                    appointment_date = appointment_date,
                    service_type = service_type
                )
                
                return Response({'message':'created successfully'},status=status.HTTP_201_CREATED)
            
        return Response({'Error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'m':str(e)},status=status.HTTP_400_BAD_REQUEST)



            








