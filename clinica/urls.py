from django.urls import path
from .views import *
app_name = "veterinaria"
urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('cita/', cita, name="citas"),
    path('doc/', doctor, name="doctor"),
    path('pet/', pet, name="pet"),
    path('citas/', citas, name="c_cita"),
    path('user/', user, name="user"),
    
]
