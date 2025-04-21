from django.urls import path
from . import views


urlpatterns=[
    path('new-doctor/',views.create_doctor),
    path('new-nurse/',views.create_new_nurse),
    path('new-clinic/',views.create_clinic),
    path('new-patient/',views.create_new_patient),
    path('appointment/',views.create_appointment),
    path('doctors/',views.doctors),
]