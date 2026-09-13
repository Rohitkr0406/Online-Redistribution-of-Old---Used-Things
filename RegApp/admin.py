from django.contrib import admin
from .models import DonorReg, UnusedThing

@admin.register(DonorReg)
class DonorRegAdmin(admin.ModelAdmin):
    list_display = ('donorid', 'dname', 'dmob', 'demail', 'city', 'state', 'userrole')
    search_fields = ('donorid', 'dname', 'demail', 'dmob', 'city')
    list_filter = ('userrole', 'gen', 'state')
    ordering = ('slno',)


@admin.register(UnusedThing)
class UnusedThingAdmin(admin.ModelAdmin):
    list_display = ('proid', 'proname', 'procate', 'prosubcate', 'purchdate', 'status', 'donorid')
    search_fields = ('proid', 'proname', 'procate', 'prosubcate', 'donorid')
    list_filter = ('procate', 'status', 'purchdate')
    ordering = ('-purchdate', 'slno')
