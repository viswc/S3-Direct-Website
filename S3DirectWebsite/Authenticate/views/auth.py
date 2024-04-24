from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from urllib.parse import urlencode
from Authenticate.models import *
import re

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            _Account = Account.objects.get(Username = user)
            if not _Account.isActive:
                queryParameter = {"error": "Account is not active"}
                return HttpResponseRedirect(reverse('Authenticate:LoginPage') + "?" + urlencode(queryParameter))
            auth_login(request, user)
            return HttpResponseRedirect(reverse("Public:HomePage"))
        else:
            queryParameter = {"error": "Invalid username or password"}
            return HttpResponseRedirect(reverse('Authenticate:LoginPage') + "?" + urlencode(queryParameter))
    else:
        return render(request, "Authenticate/login.html")
    
def logout(request):
    if request.user.is_authenticated:
      auth_logout(request)
    return HttpResponseRedirect(reverse("Public:HomePage"))

def createAccount(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        email = request.POST.get("email")
        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")

        if User.objects.filter(username = username).exists():
            queryParameter = {"error": "Username already exists"}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter)) 
        if Account.objects.filter(email = email).exists():
            queryParameter = {"error": "Email already exists"}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter))
        if username == "" or password == "" or email == "" or firstName == "" or lastName == "":
            queryParameter = {"error": "Please fill out all fields"}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter))
        
        if not re.search(r'[A-Z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*]', password) or len(password) < 8 or password != confirmPassword:
            queryParameter = {'error': 'Passwords does not match or does not meet the requirements. Passwords must be at least 8 characters long, contain at least one uppercase letter, one number and one special character.'}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter))
        if not re.match(r'^[a-zA-Z]', username) or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', username) or len(username) < 4:
            queryParameter = {'error': 'Username does not meet the requirements.'}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter))
        if not re.match(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', email):
            queryParameter = {'error': 'Email address does not meet the requirements.'}
            return HttpResponseRedirect(reverse('Authenticate:CreateAccount') + "?" + urlencode(queryParameter)) 

        user = User.objects.create_user(username = username.lower(), password = password)
        account = Account.objects.create(Username = user, email = email.lower(), firstName = firstName, lastName = lastName, isActive = True)
        queryParameter = {"success": "Account created successfully"}
        return HttpResponseRedirect(reverse('Authenticate:LoginPage') + "?" + urlencode(queryParameter))
    else:
        return render(request, "Authenticate/createAccount.html")
    
def forgotPassword(request):
    pass