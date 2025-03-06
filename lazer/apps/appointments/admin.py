from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient','appointment_date','status','created_at')
    search_fields = ('patient', 'appointment_date', 'status')
    list_filter = ('status',)
    ordering=['id','appointment_date']

admin.site.register(Appointment,AppointmentAdmin)