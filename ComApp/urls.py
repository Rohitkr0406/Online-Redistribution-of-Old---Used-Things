from django.urls import path
from . import views

urlpatterns = [
    path('Complaint', views.Complaint),
    path('CompSave', views.CompSave, name="CompSave1"),
    path('Contactus', views.Contactus),
    path('ContactSave', views.ContactSave, name="ContactSave1"),
]
