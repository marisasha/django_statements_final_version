from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.cache import caches
from django_app import models
from django_settings import utils
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import re

RamCache = caches["default"]


def home(request):
    if request.method == "GET":
        return render(
                        request=request,
                        template_name="form.html",
                        context={}
        )
    elif  request.method == "POST":
        name = request.POST["name"]
        report = request.POST["report_text"]
        
        models.Report.objects.create(name=name,report_text=report)
        return render(
                        request=request,
                        template_name="form.html",
                        context={}
                    )

def statements(request):
    _data = lambda: utils.native_paginate(request, models.Report.objects.all().order_by("-id"), 100) 
    obj = utils.get_cache(f"statements {request.GET.get('page', 1)}", lambda: _data(), timeout=5)  
    return render(
                    request=request,
                    template_name="statements.html",
                    context={"obj":obj}
                )


    

def statement(request,pk: str):
    obj = utils.get_cache(f"statement ", lambda: models.Report.objects.get(id=int(pk)), timeout=2)
    return render(
                    request=request,
                    template_name="statement.html",
                    context={"obj":obj}
                )

def statement_delete(request,pk: str):
    models.Report.objects.get(id=int(pk)).delete()

    return redirect(reverse("statements"))

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        password_accept = str(request.POST["password_accept"])
        if password != password_accept:
            return render(request, "register.html", context={"error": "Пароли не совпадают!"})
        usr = User.objects.create(username=username, password=make_password(password))
        login(request, usr) 
        return redirect(reverse("statements"))


def login_v(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = str(request.POST["username"])  # из формы
        password = str(request.POST["password"])  # из формы
        print(username)


        # аутентификация - проверяет наличие пользователя с таким логин+пароль
        # авторизация - проверят права
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return render(request, "login.html", context={"error": "Логин или пароль не совпадают!"})
        login(request, user)
        return redirect(reverse("statements"))

def logout_v(request):
    logout(request)
    return redirect(reverse("login"))





