from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import utils

#-----------------------------------------------------------------------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email="", name="", family="", active_code=None, gender=None, password=None, is_active=False):
        if not mobile_number:
            raise ValueError("شماره موبایل باید وارد شود")
        if not active_code:
            active_code = utils.creat_random_code(5) 
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            gender=gender,
            active_code=active_code,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email, name, family, password=None, active_code=None, gender=None):
        user = self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password,
            is_active=True,
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


#-----------------------------------------------------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('patient', 'بیمار'),
        ('receptionist', 'منشی'),
        ('doctor', 'دکتر'),
    )
    
    mobile_number = models.CharField(max_length=11, unique=True,verbose_name='شماره موبایل')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    name = models.CharField(max_length=100, blank=True, null=True)
    family = models.CharField(max_length=100, blank=True, null=True)
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=50,choices=GENDER_CHOICES,default='True',null=True,blank=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    active_code=models.CharField(max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'family', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} {self.family} - {self.role}"
    
    @property
    def is_staff(self):
        return self.is_admin

