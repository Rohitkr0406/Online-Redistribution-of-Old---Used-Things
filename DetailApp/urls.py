from django.urls import path
from . import views

urlpatterns = [
    # Collection Routes
    path('Collection', views.Collection),
    path('CollectionSave', views.CollectionSave, name="CollectionSave1"),
    path('CollectionDelete', views.CollectionDelete, name="CollectionDelete1"),
    path('CollectionSearch', views.CollectionSearch, name="CollectionSearch1"),
    path('CollectionUpdate', views.CollectionUpdate, name="CollectionUpdate1"),
    
    # Stock Routes
    path('Stock', views.Stock),
    path('StockSave', views.StockSave, name="StockSave1"),
    path('StockSearch', views.StockSearch, name="StockSearch1"),
    path('StockDelete', views.StockDelete, name="StockDelete1"),
    path('StockUpdate', views.StockUpdate, name="StockUpdate1"),
    
    # Distribution Routes
    path('Distribution', views.Distribution),
    path('DistributionSave', views.DistributionSave, name="DistributionSave1"),
    path('DistributionDelete', views.DistributionDelete, name="DistributionDelete1"),
    path('DistributionSearch', views.DistributionSearch, name="DistributionSearch1"),
    path('DistributionUpdate', views.DistributionUpdate, name="DistributionUpdate1"),
]
