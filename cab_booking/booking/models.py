from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class DriverManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)

class Driver(AbstractBaseUser):
    username = models.CharField(max_length=10, primary_key= True)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    latitude =  models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)
    vehicle_number = models.CharField(max_length=10)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = DriverManager()
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def __str__(self):
        return str(self.username)

class Customer(models.Model):
    username = models.CharField(max_length=30, primary_key= True)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    latitude =  models.FloatField(default= 0)
    longitude = models.FloatField(default= 0)
    
    USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'username'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def __str__(self):
        return str(self.username)

    
class RideRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    customer = models.CharField(max_length=20)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return str(self.customer) + " - " + str(self.status)
    
