from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        if ('pwd2' in request.POST):
            user = User.objects.create_user(username = request.POST['usr'], password = request.POST['pwd'], email = request.POST['email'])
            user.save()
            return redirect("/login/")
        else:
            user = auth.authenticate(username = request.POST['usr'], password = request.POST['pwd'])    #hacerlo con email
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