from django.contrib import admin
from .models import CollectionTable, StockDetails, DistributeTable, Recipient, DonationRequest

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


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('recipient_id', 'name', 'mobile', 'email', 'city', 'state', 'date_joined')
    search_fields = ('recipient_id', 'name', 'email', 'mobile', 'city')
    list_filter = ('state', 'city', 'date_joined')
    ordering = ('recipient_id',)


@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'recipient', 'item', 'req_date', 'status')
    search_fields = ('req_id', 'recipient__name', 'recipient__recipient_id', 'item__proid', 'item__proname')
    list_filter = ('status', 'req_date')
    ordering = ('-req_date', 'req_id')
