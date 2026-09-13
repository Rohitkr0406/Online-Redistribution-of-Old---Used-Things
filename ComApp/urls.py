from django.urls import path
from . import views

urlpatterns = [
    path('Complaint', views.Complaint, name="Complaint1"),
    path('CompSave', views.CompSave, name="CompSave1"),
    path('Contactus', views.Contactus, name="Contactus1"),
    path('ContactSave', views.ContactSave, name="ContactSave1"),
]
