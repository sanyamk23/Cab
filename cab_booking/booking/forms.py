from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer, Driver, RideRequest

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password']

class DriverRegistrationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ['username', 'email', 'password', 'vehicle_number']

class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password']

class DriverLoginForm(AuthenticationForm):
    class Meta:
        model = Driver
        fields = ['username', 'password']

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['customer', 'pickup_location', 'dropoff_location']