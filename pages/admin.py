from django.contrib import admin

from .models import Clients


class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'email', 'date_pub', 'processed')
    search_fields = ('name', 'number', 'email', 'date_pub')
    list_filter = ['processed']


admin.site.register(Clients, SettingAdmin)
