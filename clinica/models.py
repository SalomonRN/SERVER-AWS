from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Genders(models.TextChoices):
        FAMELE = "M","Mujer"
        MALE = "H","Hombre"

class Doctor(models.Model):
    
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    age = models.PositiveSmallIntegerField(default=0)
    gender = models.CharField(max_length=10, choices=Genders.choices, default="")
    specialization = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        
class Mascota(models.Model):
    class Type(models.TextChoices):
        CAT = "CAT", "Gato"
        DOG = "DOG", "Perro"
        PARROT = "PRT", "Loro"
        TURTLE = "TRL", "Tortuga"
        OTHER = "Ot", "Otro animal"
        
    name = models.CharField(max_length=45)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=Type.choices, max_length=45, default="")
    
    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

class Cita(models.Model):
    description = models.CharField(max_length=45)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return f"Cita hecha por {self.client} para su mascota {self.pet.name}, con el doctor {self.doctor}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=45)

    def __str__(self):
        return self.user.username
