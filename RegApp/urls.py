from django.urls import path
from . import views

urlpatterns = [
    path('Donator', views.Donator, name="Donator1"),
    path('DonatorSave', views.DonatorSave, name="DonatorSave1"),
    path('DonatorDelete', views.DonatorDelete, name="DonatorDelete1"),
    path('DonatorSearch', views.DonatorSearch, name="DonatorSearch1"),
    path('DonatorUpdate', views.DonatorUpdate, name="DonatorUpdate1"),
    path('Unused', views.Unused, name="Unused1"),
    path('UnusedSave', views.UnusedSave, name="UnusedSave1"),
    path('UnusedDelete', views.UnusedDelete, name="UnusedDelete1"),
    path('UnusedSearch', views.UnusedSearch, name="UnusedSearch1"),
    path('UnusedUpdate', views.UnusedUpdate, name="UnusedUpdate1"),
]
