from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Authenticate.models import *

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
        return render(request, 'Public/Home.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))