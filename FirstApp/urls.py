from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('ConnecivityPage', views.ConnecivityPage),
    path('Login', views.Login),
    path('Demo', views.Demo),
]
