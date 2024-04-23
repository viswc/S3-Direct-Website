from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "Public"
urlpatterns = [
     path("", Home.home, name = "HomePageReverse"),
     path("home/", Home.home, name = "HomePage"),
]