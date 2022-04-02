from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import User

import re

# Create your views here.

def login(request):
    if(request.user.is_authenticated):
        auth.logout(request)

    if request.method == 'POST':
        user = auth.authenticate(email = request.POST['email'], password = request.POST['pwd'])
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            return render(request, "login.html",{"message":"Usuario y/o contraseña incorrecto."}, status = 401)
    else:
        return render(request, "login.html", status = 200)


def register(request):
    if(request.user.is_authenticated):
        auth.logout(request)
        
    parameters = dict()
    if request.method == 'POST':
        if not checkPassword(request.POST['pwd1'], request.POST['pwd2']):
            parameters['message_pwd'] = ('La contraseña no cumple los requisitos.')
        if not len(User.objects.filter(email=request.POST['email'])) == 0:
            parameters['message_email'] = ('Ese email ya está en uso.')
        if not len(User.objects.filter(nick=request.POST['nick'])) == 0:
            parameters['message_nick'] = ('Ese nick ya está en uso.')

        if len(parameters) == 0:
            user = User.objects.create_user(email = request.POST['email'], password = request.POST['pwd1'], nick = request.POST['nick'])
            user.save()
            auth.login(request,user)
            return redirect("/")
        else:
            return render(request, "register.html", parameters, status = 400)
    else:
        return render(request, "register.html", status = 200)


def logout(request):
    auth.logout(request)
    return redirect("/")


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            parameters = dict()
            user = request.user

            if 'delete-img' in request.POST:
                if request.POST['delete-img'] == 'true':
                    user.user_img.delete()
                    user.user_img = ""

            if 'user_img' in request.FILES:
                if user.user_img != "":
                    user.user_img.delete()
                image = request.FILES['user_img']
                image.name = user.nick + image.name[image.name.find('.'):len(image.name)]
                user.user_img = image

            if 'pwd1' in request.POST and len(request.POST['pwd1'])!= 0:
                print(checkPassword(request.POST['pwd1'],request.POST['pwd2']))
                if checkPassword(request.POST['pwd1'], request.POST['pwd2']):
                    user.set_password(request.POST['pwd1'])
                else:
                    parameters['message_pwd'] = ('La contraseña no cumple los requisitos.')

            if 'nick' in request.POST:
                if len(User.objects.filter(nick=request.POST['nick'])) == 0:
                    user.nick = request.POST['nick']
                else:
                    parameters['message_nick'] = ('El nick "%s" no está disponible.' % request.POST['nick'])

            user.save()
            return render(request, "profile.html", parameters)
        else:
            return render(request, "profile.html")
    else:
        return render(request, "login.html")








class WrongPassword(Exception):
    def __message__(self):
        return "The two password are diferent."

def checkPassword(pwd1 = str(), pwd2 = str()):
    return ((pwd1 == pwd2) and (len(pwd1) > 10) and (re.search("[a-z]", pwd1)) and (re.search("[A-Z]", pwd1)) and (re.search("[0-9]", pwd1)))