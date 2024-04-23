from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# from Authenticate.models import *

def home(request):
    if request.method == 'GET':
        return render(request, 'Public/Home.html')
    else:
        return HttpResponseRedirect(reverse('Public:HomePage'))