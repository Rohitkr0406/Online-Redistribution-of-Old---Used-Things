from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportHome),
    path('StockReport', views.StockReport),
    path('StockReportSearch', views.StockReportSearch, name="StockReportSearch1"),
    path('DonorReport', views.DonorReport),
    path('DonorReportSearch', views.DonorReportSearch, name="DonorReportSearch1"),
    path('UnusedReport', views.UnusedReport),
    path('UnusedReportSearch', views.UnusedReportSearch, name="UnusedReportSearch1"),
    path('CollectionReport', views.CollectionReport),
    path('CollectionReportSearch', views.CollectionReportSearch, name="CollectionReportSearch1"),
    path('DistributionReport', views.DistributionReport),
    path('DistributionReportSearch', views.DistributionReportSearch, name="DistributionReportSearch1"),
    path('ComplaintReport', views.ComplaintReport),
    path('ComplaintReportSearch', views.ComplaintReportSearch, name="ComplaintReportSearch1"),
    path('ContactUsReport', views.ContactUsReport),
    path('ConReportSearch', views.ConReportSearch, name="ConReportSearch1"),
]
