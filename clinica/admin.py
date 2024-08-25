from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    pass

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    pass
