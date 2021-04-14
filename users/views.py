from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from .models import User


# Create your views here.

def login(request):
    if request.method == 'POST':
        if ('pwd2' in request.POST):
            #user = User.objects.create_user(username = request.POST['usr'], password = request.POST['pwd'], email = request.POST['email'])
            user = User.objects.create_user(email = request.POST['email'], password = request.POST['pwd'], nick = request.POST['nick'])
            user.save()
            return redirect("/login/")
        else:
            user = auth.authenticate(email = request.POST['email'], password = request.POST['pwd'])    #hacerlo con email
            if user is not None:
                auth.login(request,user)
                #return redirect("/")
                return redirect("/admin/")
            else:
                return render(request, "login.html")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    #return redirect("/")
    return redirect("/admin/")

def profile(request):
    return render(request, "profile.html")