from django.db import models
from django.conf import settings
from apps.accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

# -----------------------------------------------------------------------------------------------------------------------
class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedules', limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')


    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("زمان شروع باید قبل از زمان پایان باشد.")


    def __str__(self):
        return f"{self.doctor.name} {self.doctor.family} - {self.date} ({self.start_time} to {self.end_time})"



# -----------------------------------------------------------------------------------------------------------------------
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('canceled', 'لغو شده'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    schedule = models.ForeignKey(DoctorSchedule,null=True, blank=True, on_delete=models.CASCADE, related_name='doctor_schedule')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    # class Meta:
    #     unique_together = ('doctor', 'appointment_date')  # جلوگیری از تداخل نوبت دکتر در یک زمان مشخص

    def clean(self):
        """
        بررسی می‌کند که تاریخ و زمان انتخاب‌شده در بازه زمانی دکتر باشد.
        """
        # چک می‌کنیم که برنامه زمان‌بندی متعلق به دکتر باشد
        if self.schedule.doctor != self.doctor:
            raise ValidationError("برنامه زمان‌بندی انتخاب‌شده متعلق به این دکتر نیست!")

        # چک کردن اینکه تاریخ نوبت با تاریخ برنامه دکتر یکی باشد
        appointment_date_only = localtime(self.appointment_date).date()
        if appointment_date_only != self.schedule.date:
            raise ValidationError("تاریخ انتخاب‌شده با برنامه زمان‌بندی دکتر مطابقت ندارد!")

        # چک کردن اینکه ساعت نوبت در بازه زمانی باشد
        appointment_time = localtime(self.appointment_date).time()
        if not (self.schedule.start_time <= appointment_time <= self.schedule.end_time):
            raise ValidationError("ساعت انتخاب‌شده خارج از ساعات کاری دکتر است!")

    def __str__(self):
        return f"{self.patient.name} {self.patient.family} - {self.doctor.name} ({self.appointment_date})"
