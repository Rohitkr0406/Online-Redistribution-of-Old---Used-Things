from django.contrib import admin
from .models import CollectionTable, StockDetails, DistributeTable

@admin.register(CollectionTable)
class CollectionTableAdmin(admin.ModelAdmin):
    list_display = ('proid', 'collqty', 'recdate', 'status', 'donby', 'recby')
    search_fields = ('proid', 'donby', 'recby', 'donoradd')
    list_filter = ('status', 'recdate')
    ordering = ('-recdate', 'slno')


@admin.register(StockDetails)
class StockDetailsAdmin(admin.ModelAdmin):
    list_display = ('proid', 'pname', 'cate', 'subcate', 'stockamt', 'disamt')
    search_fields = ('proid', 'pname', 'cate', 'subcate', 'proslno', 'batchno')
    list_filter = ('cate',)
    ordering = ('slno',)


@admin.register(DistributeTable)
class DistributeTableAdmin(admin.ModelAdmin):
    list_display = ('proid', 'disqty', 'disdate', 'recname', 'recmob', 'disby')
    search_fields = ('proid', 'recname', 'recmob', 'recadd', 'disby', 'recby')
    list_filter = ('disdate',)
    ordering = ('-disdate', 'slno')
