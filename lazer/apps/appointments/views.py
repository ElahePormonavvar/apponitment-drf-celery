from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from . permisssions import IsDoctorOrStaff


class AppointmentViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient=user)
            
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated,IsDoctorOrStaff]

