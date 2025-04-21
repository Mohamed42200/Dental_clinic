from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from rest_framework.response import Response

#models
from .models import Doctor, Clinic,Nurse,Patient,Apointment



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','confirm_password']
    def validate(self, attrs):
        if attrs['password']!=attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

  
class Create_Doctor_Serializer(serializers.ModelSerializer):
    user = UserSerializer()   #contains ['username', 'email', 'password'] 
    clinic_name = serializers.CharField()  
         

    class Meta:
       model = Doctor
       fields=['user','phone', 'specialization', 'qualification','clinic_name']

class Create_Nurse_Serializer(serializers.ModelSerializer):
    user = UserSerializer()
    clinic_name = serializers.CharField()

    class Meta:
        model = Nurse
        fields =['user','phone','clinic_name']


class create_patient_serializer(serializers.ModelSerializer):
    user = UserSerializer()
    clinic_name = serializers.CharField()  

    class Meta:
        model = Patient
        fields = ['user','photo','phone','address','clinic_name']


class Appointment_Serializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Apointment
        fields = ['user','appointment_date','service_type']
        





class Create_Clinic_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Clinic
        fields = '__all__'



