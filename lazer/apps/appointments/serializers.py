from rest_framework import serializers
from django.utils.timezone import now 
from .models import DoctorSchedule, Appointment
from apps.accounts.models import CustomUser
# ----------------------------------------------------------------------------

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    doctor = serializers.ReadOnlyField(source='schedule.doctor.id')
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_date', 'doctor', 'schedule', 'status', 'created_at']

    def validate_appointment_date(self, value):
        if value <= now():
            raise serializers.ValidationError("The appointment date must be in the future.")
        return value

# ----------------------------------------------------------------------------
class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_available']
