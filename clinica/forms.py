import datetime
from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import boto3
from os import getenv
class LoginForm(AuthenticationForm):
    pass

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        super().__init__(*args, **kwargs)
        
        if client_id:
            #self.fields['pet'] accede al campo pet del formulario
            self.fields['owner'].queryset = User.objects.filter(id=client_id) 
    
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        super().__init__(*args, **kwargs)
        
        if client_id:
            #self.fields['pet'] accede al campo pet del formulario
            self.fields['pet'].queryset = Mascota.objects.filter(owner_id=client_id)
            self.fields['client'].queryset = User.objects.filter(id=client_id) 

class SignupForm(UserCreationForm):
    photo = forms.ImageField(required=False)
       
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    