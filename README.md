# Clinic Appointment System

Built with Django REST Framework.

## Features

- User registration and authentication with JWT tokens
- Appointment Management: Full CRUD operations for booking, updating, and cancelingappointments via API
- Automated Appointment Reminders: Scheduled SMS notifications to remind users of their upcoming appointments
- Using SmsIr API to send SMS

## Installation

- Python 3.x
- Django 3.x or later
- MySQL

## Requirements

amqp==5.3.1
asgiref==3.8.1
billiard==4.2.1
celery==5.4.0
certifi==2024.12.14
charset-normalizer==3.4.1
click==8.1.8
click-didyoumean==0.3.1
click-plugins==1.1.1
click-repl==0.3.0
colorama==0.4.6
cron-descriptor==1.4.5
Django==5.1.4
django-celery-beat==2.7.0
django-ckeditor==6.7.2
django-ckeditor-5==0.2.15
django-cors-headers==4.7.0
django-environ==0.12.0
django-jazzmin==3.0.1
django-js-asset==3.0.1
django-timezone-field==7.1
djangorestframework==3.15.2
djangorestframework_simplejwt==5.4.0
idna==3.10
kombu==5.4.2
mysql-connector-python==9.1.0
pillow==11.1.0
prompt_toolkit==3.0.48
PyJWT==2.10.1
python-crontab==3.2.0
python-dateutil==2.9.0.post0
redis==5.2.1
requests==2.32.3
six==1.17.0
smsir-python==1.0.8
sqlparse==0.5.3
tzdata==2024.2
urllib3==2.3.0
vine==5.1.0
wcwidth==0.2.13


### Clone the repository

```bash
git clone https://github.com/ElahePormonavvar/apponitment-drf-celery.git
cd lazer