from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AdminLogin, name='admin_login'),
    path('dashboard/', views.AdminDashboard, name='admin_dashboard'),
    path('logout/', views.AdminLogout, name='admin_logout'),
    path('donors/', views.AdminDonorManagement, name='admin_donors'),
    path('items/', views.AdminItemsManagement, name='admin_items'),
    path('settings/', views.AdminSettings, name='admin_settings'),
]
