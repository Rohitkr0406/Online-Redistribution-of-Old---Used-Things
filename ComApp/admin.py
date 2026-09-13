from django.contrib import admin
from .models import ComplaintTable, ContactUs

@admin.register(ComplaintTable)
class ComplaintTableAdmin(admin.ModelAdmin):
    list_display = ('did', 'compdate', 'issutype', 'compdetails', 'remarks')
    search_fields = ('did', 'issutype', 'compdetails', 'remarks')
    list_filter = ('issutype', 'compdate')
    ordering = ('-compdate', 'slno')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('admid', 'comname', 'comemail', 'commob', 'comadd')
    search_fields = ('admid', 'comname', 'comemail', 'commob', 'comadd')
    ordering = ('slno',)
