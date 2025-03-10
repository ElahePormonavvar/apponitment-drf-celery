from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, DoctorScheduleCreateView, DoctorScheduleListView

app_name = 'appointments'
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = router.urls + [
    path('schedules/', DoctorScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', DoctorScheduleCreateView.as_view(), name='schedule-create'),
]
