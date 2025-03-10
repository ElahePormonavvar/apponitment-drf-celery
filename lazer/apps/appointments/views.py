from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer,DoctorScheduleSerializer
from . permisssions import IsDoctorOrStaff,IsDoctor,IsReceptionistOrDoctor,IsPatient
from rest_framework import generics
from .models import DoctorSchedule
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

# ----------------------------------------------------------------------------
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from apps.appointments.models import Appointment, DoctorSchedule
from apps.accounts.models import CustomUser
from apps.appointments.serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        
        if user.role in ['doctor', 'receptionist']:
            return Appointment.objects.all()
        
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        
        return Appointment.objects.none()

    def perform_create(self, serializer):
        try:
            schedule_id = self.request.data.get('schedule')
            if not schedule_id:
                return Response({"error": "شناسه برنامه زمانی ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)

            schedule = DoctorSchedule.objects.get(id=schedule_id)

            appointment_date_str = self.request.data.get('appointment_date')
            if not appointment_date_str:
                return Response({"error": "تاریخ نوبت ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                return Response({"error": "فرمت تاریخ نامعتبر است. فرمت صحیح: YYYY-MM-DDTHH:MM:SSZ"}, status=status.HTTP_400_BAD_REQUEST)

            if schedule.start_time and schedule.end_time:
                if not (schedule.start_time <= appointment_date.time() <= schedule.end_time):
                    return Response({"error": "زمان انتخابی خارج از ساعات کاری دکتر است."}, status=status.HTTP_400_BAD_REQUEST)

            if Appointment.objects.filter(schedule=schedule, appointment_date=appointment_date).exists():
                return Response({"error": "این زمان قبلاً رزرو شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # اگر کاربر خود بیمار است، از خود درخواست استفاده کن
            patient = self.request.user if self.request.user.role == 'patient' else CustomUser.objects.filter(id=self.request.data.get('patient')).first()

            if not patient:
                return Response({"error": "بیمار مشخص نشده است."}, status=status.HTTP_400_BAD_REQUEST)

            if not schedule.is_available:
                return Response({"error": "این زمان قبلاً رزرو شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # ذخیره نوبت
            appointment = serializer.save(
                patient=patient,
                doctor=schedule.doctor,
                schedule=schedule,
                appointment_date=appointment_date
            )
            serializer.save(patient=patient, doctor=schedule.doctor, schedule=schedule, appointment_date=appointment_date)
            schedule.is_available = False
            schedule.save()

            return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

        except DoctorSchedule.DoesNotExist:
            return Response({"error": "برنامه زمانی یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"خطای غیرمنتظره: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsReceptionistOrDoctor]
        self.check_permissions(request)

        instance = self.get_object()
        new_status = request.data.get('status')

        if new_status in ['confirmed', 'canceled']:
            instance.status = new_status
            instance.save()
            return Response({"message": "وضعیت نوبت به‌روزرسانی شد."}, status=status.HTTP_200_OK)

        return Response({"error": "وضعیت نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------------
class DoctorScheduleCreateView(generics.CreateAPIView):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [IsAuthenticated,IsDoctor]
    
    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            return Response({"error": "تنها پزشکان می‌توانند برنامه زمانی اضافه کنند."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(doctor=self.request.user)

# ----------------------------------------------------------------------------
class DoctorScheduleListView(generics.ListAPIView):
    serializer_class = DoctorScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorSchedule.objects.filter(is_available=True)
    
# ---------------------------------------------------------------------------
