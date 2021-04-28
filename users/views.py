from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from .models import User

from django.core.files.storage import default_storage

# Create your views here.

def login(request):
    if request.method == 'POST':
        if ('pwd2' in request.POST):
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

            aux = User.objects.filter(nick="admin")
            print(len(aux))
            if 'nick' in request.POST:
                if len(User.objects.filter(nick=request.POST['nick'])) == 0:
                    user.nick = request.POST['nick']
                else:
                    parameters['message'] = ('El nick "%s" no está disponible.' % request.POST['nick'])

            user.save()
            return render(request, "profile.html", parameters)
        else:
            return render(request, "profile.html")
    else:
        return render(request, "login.html")  


class WrongPassword(Exception):
    def __message__(self):
        return "The two password are diferent."