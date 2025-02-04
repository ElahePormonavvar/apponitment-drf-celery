from rest_framework import serializers
from .models import Appointment
from django.contrib.auth import get_user_model
from django.utils.timezone import now 

# ----------------------------------------------------------------------------
User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'status']

    def validate_appointment_date(self, value):
        if value <= now():
            raise serializers.ValidationError("The appointment date must be in the future.")
        return value
