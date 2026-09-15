from django.urls import path
from . import views

urlpatterns = [
    # Recipient Authentication
    path('RecipientRegister', views.RecipientRegister, name='RecipientRegister'),
    path('RecipientLogin', views.RecipientLogin, name='RecipientLogin'),
    path('RecipientLogout', views.RecipientLogout, name='RecipientLogout'),

    # Available Stock / Catalog
    path('AvailableItems', views.AvailableItems, name='AvailableItems'),

    # Item Request System
    path('RequestItem/<str:proid>', views.RequestItem, name='RequestItem'),
    path('MyRequests', views.MyRequests, name='MyRequests'),

    # Administrator Management & Distribution
    path('AdminRequests', views.AdminRequests, name='AdminRequests'),
    path('ApproveRequest/<str:req_id>', views.ApproveRequest, name='ApproveRequest'),
    path('RejectRequest/<str:req_id>', views.RejectRequest, name='RejectRequest'),
    path('DistributeRequest/<str:req_id>', views.DistributeRequest, name='DistributeRequest'),

    # SRS Operational Reports Module (Admin-only)
    path('Reports/', views.ReportHome, name='ReportHome'),
    path('Reports/DonorRegistration/', views.DonorReport, name='DonorReport'),
    path('Reports/UnusedThings/', views.UnusedReport, name='UnusedReport'),
    path('Reports/Collection/', views.CollectionReport, name='CollectionReport'),
    path('Reports/Stock/', views.StockReport, name='StockReport'),
    path('Reports/Distribution/', views.DistributionReport, name='DistributionReport'),
    path('Reports/Complaints/', views.ComplaintReport, name='ComplaintReport'),
    path('Reports/ContactUs/', views.ContactUsReport, name='ContactUsReport'),
]
