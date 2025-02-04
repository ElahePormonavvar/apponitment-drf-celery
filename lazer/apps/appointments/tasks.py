from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import Appointment
from utils import send_sms2


@shared_task(max_retries=0)
def send_appointment_reminder():
    tomorrow = now() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        appointment_date__date=tomorrow.date(),
        status='confirmed'
        )
    
    if not appointments.exists():
        return "There are no confirmed appointments to remind."
    
    for appointment in appointments:        
        patient_name = f"{appointment.patient.name} {appointment.patient.family}".strip()
        if not patient_name:
            patient_name = "Dear patient"
        message= f"{patient_name} Dear, your laser appointment is tomorrow at {appointment.appointment_date.strftime('%H:%M')} Please arrive 10 minutes early at Dr.Ela's Laser Clinic."        
        send_sms2(appointment.patient.mobile_number, message)
    return f"{appointments.count()} Message sent."

