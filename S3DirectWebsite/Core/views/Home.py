from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Authenticate.models import *
from Core.models import *

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            context = {
                "isAuthenticated": True,
                "Account": _Account
            }
        else:
            context = {
                "isAuthenticated": False
            }

        reqReviews = Reviews.objects.order_by('-dateCreated')[:3]
        context["Reviews"] = reqReviews
        return render(request, 'Public/Pages/Home.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))
    
def about(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            context = {
                "isAuthenticated": True,
                "Account": _Account
            }
        else:
            context = {
                "isAuthenticated": False
            }
        return render(request, 'Public/Pages/About.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))

def contact(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            context = {
                "isAuthenticated": True,
                "Account": _Account
            }
        else:
            context = {
                "isAuthenticated": False
            }
        return render(request, 'Public/Pages/Contact.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))
    
def download(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            context = {
                "isAuthenticated": True,
                "Account": _Account
            }
        else:
            context = {
                "isAuthenticated": False
            }

        reqReviews = Reviews.objects.order_by('-dateCreated')[:3]
        context["Reviews"] = reqReviews
        return render(request, 'Public/Pages/Download.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))