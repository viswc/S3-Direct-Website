from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "Public"
urlpatterns = [
     path("", Home.home, name = "HomePageReverse"),
     path("home/", Home.home, name = "HomePage"),
     path("forum/", Home.forum, name = "ForumPage"),
     path("forum/create/", Home.forumCreate, name = "ForumCreatePage"),
     path("forum/<str:slug>/", Home.forumDetail, name = "ForumDetailPage"),
     path("forum/<str:slug>/edit/", Home.forumEdit, name = "ForumEditPage"),
     path("forum/<str:slug>/delete/", Home.forumDelete, name = "ForumDeletePage"),
     path("forum/<str:slug>/comment/", Home.forumComment, name = "ForumAddComment"),
]