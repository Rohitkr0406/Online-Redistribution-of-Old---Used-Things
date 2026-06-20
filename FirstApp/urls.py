from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('ConnecivityPage', views.ConnecivityPage),
    path('Login', views.Login),
    path('Logout', views.Logout, name='donor_logout'),
    path('Demo', views.Demo),
]
