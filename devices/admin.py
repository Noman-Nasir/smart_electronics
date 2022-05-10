from django.contrib import admin

from .models import Device


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['device_type']
    search_fields = ['name', 'price', 'description', 'manufacturer']


admin.site.register(Device, ItemAdmin)
