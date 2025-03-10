from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('mobile_number','role', 'email', 'name', 'family', 'is_active', 'is_admin')
    search_fields = ('mobile_number', 'role', 'name', 'family')
    list_filter = ('is_active', 'is_admin')
    ordering=['id']

admin.site.register(CustomUser, CustomUserAdmin)