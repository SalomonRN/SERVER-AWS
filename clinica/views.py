from .serializer import *
import boto3
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from os import getenv
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.core import signing
@csrf_exempt
def logind(request):
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("veterinaria:home")
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, "index.html", {"form": form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    else:
        return logind(request)        

@csrf_exempt
@login_required(login_url="/")
def home(request):
    return render(request, "home.html")

@csrf_exempt
@login_required(login_url="/")
def logout(request):
    auth_logout(request)
    return redirect("veterinaria:login")

@csrf_exempt
def cita(request: HttpRequest):
    if request.method == "POST":
        data = request.POST.copy()
        data['pet'] = Mascota.objects.get(name=data['pet'])
        data['client'] = request.session['_auth_user_id']

        cita = CitaForm(data, client_id=request.session['_auth_user_id'])
        if cita.is_valid():
                cita.save()
                return JsonResponse({"message" : "CITA GUARDAA"})
        else:
            return JsonResponse(cita.errors)
    elif request.method == "GET":
        form = CitaForm(client_id=request.session["_auth_user_id"])
        return render(request, "cita.html", {"form": form,})

@csrf_exempt
def pet(request: HttpRequest):
    if request.method == "POST":
        data = request.POST.copy()
        data['owner'] = request.session['_auth_user_id']
        pet = MascotaForm(data)
        if pet.is_valid():
            pet.save()
            return JsonResponse({"message": "REGISTRADO"})
        else:
            print(pet.errors)
            return JsonResponse(pet.errors)
        
       
    elif request.method == "GET":
        form = MascotaForm(client_id=request.session["_auth_user_id"])
        return render(request, "pet.html", {"form": form,},)

@csrf_exempt
@login_required(login_url="/")
@api_view(['GET'])
def citas(request):
    citas = Cita.objects.filter(client=User.objects.get(id=request.session["_auth_user_id"]))
    serializer = CitaSerializer(citas, many=True)
    return Response(serializer.data)

@csrf_exempt
@login_required
@staff_member_required
def doctor(request: HttpRequest):

    return HttpResponse("JH")

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        if not request.FILES.get('photo'): return HttpResponse("SUBA UN ARCHIVO")
        try:
            time = "-".join(str(datetime.datetime.now()).split(" "))
            s3 = boto3.client('s3',aws_access_key_id="KEY", aws_secret_access_key="KEY")
            s3.upload_file(request.FILES.get('photo').temporary_file_path(), 'bucket-20.08.2004', f'{time}.png', ExtraArgs={'ACL': 'public-read'})
        except Exception as e:
            print(e)
            print("ALGO SALIÓ MAL...")
            
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, photo=f"{time}")
            return JsonResponse({"message":"Registrado"})
        else:
            print(form.errors)
            return JsonResponse(form.errors)
    else:
        form = SignupForm()
        print(form)
    return render(request, "signup.html", {"form": form})

def user(request: HttpRequest):

    user = Profile.objects.get(user_id=request.session['_auth_user_id'])
    print(user.photo)
    return JsonResponse({"photo": f"{user.photo}.png"})
