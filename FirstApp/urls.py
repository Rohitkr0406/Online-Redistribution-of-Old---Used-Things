from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home_firstapp'),
    path('ConnecivityPage', views.ConnecivityPage, name='connectivity'),
    path('Login', views.Login, name='login'),
    path('Logout', views.Logout, name='donor_logout'),
    path('Demo', views.Demo, name='about'),
]
