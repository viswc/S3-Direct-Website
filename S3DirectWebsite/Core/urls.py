from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "Public"
urlpatterns = [
     path("", Home.home, name = "HomePageReverse"),
     path("home/", Home.home, name = "HomePage"),
     path("about/", Home.about, name = "AboutPage"),
     path("contact/", Home.contact, name = "ContactPage"),

     path("forum/", Forum.forum, name = "ForumPage"),
     path("forum/create/", Forum.forumCreate, name = "ForumCreatePage"),
     path("forum/<str:slug>/", Forum.forumDetail, name = "ForumDetailPage"),
     path("forum/<str:slug>/action/", Forum.forumAction, name = "ForumActionPage"),
     path("forum/<str:slug>/edit/", Forum.forumEdit, name = "ForumEditPage"),
     path("forum/<str:slug>/delete/", Forum.forumDelete, name = "ForumDeletePage"),
     path("forum/<str:slug>/comment/", Forum.forumComment, name = "ForumAddComment"),

     path("reviews/", ReviewsC.reviewsFunc, name = "ReviewsPage"),
     path("reviews/update/", ReviewsC.reviewsUpdate, name = "ReviewsUpdatePage"),
]