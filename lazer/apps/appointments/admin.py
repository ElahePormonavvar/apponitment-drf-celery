from django.contrib import admin
from .models import Appointment,DoctorSchedule
from apps.accounts.models import CustomUser

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient','appointment_date','status','created_at')
    search_fields = ('patient', 'appointment_date', 'status')
    list_filter = ('status',)
    ordering=['id','appointment_date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patient":
            kwargs["queryset"] = CustomUser.objects.filter(role="patient")  # فقط بیماران نمایش داده شوند
        elif db_field.name == "doctor":
            kwargs["queryset"] = CustomUser.objects.filter(role="doctor")  # فقط دکترها نمایش داده شوند
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Appointment,AppointmentAdmin)

class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor','date','start_time','end_time','is_available')
    search_fields = ('date', 'is_available')
    list_filter = ('is_available',)
    ordering=['is_available','date']

admin.site.register(DoctorSchedule,DoctorScheduleAdmin)