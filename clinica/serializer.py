
from rest_framework import serializers
from .models import Cita

class CitaSerializer(serializers.ModelSerializer):
    pet = serializers.StringRelatedField() 
    doctor = serializers.StringRelatedField() 
    class Meta:
        model = Cita
        fields = '__all__'