from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Authenticate.models import *
from Core.models import *

def reviewsFunc(request):
    if request.method == 'GET':
        sortby, Param = str(request.GET.get('sortby')), None
        if sortby.endswith('date'):
            if sortby.startswith('asc'):
                Param = 'dateCreated'
            else:
                Param = '-dateCreated'
        else:
            if sortby.startswith('asc'):
                Param = 'Rating'
            else:
                Param = '-Rating'

        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            UserReviews = Reviews.objects.filter(Profile = _Account).first()
            _Reviews = Reviews.objects.exclude(Profile = _Account).order_by(Param)

            context = {
                "isAuthenticated": True,
                "Account": _Account,
                "UserReviews": UserReviews,
                "Reviews": _Reviews
            }

        else:
            _Reviews = Reviews.objects.all().order_by(Param)
            context = {
                "isAuthenticated": False,
                "Reviews": _Reviews
            }
        return render(request, 'Public/Reviews/Reviews.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:ReviewsPage'))
    
def reviewsUpdate(request):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        if request.method == 'POST':
            Content = request.POST.get('Content')
            Rating = int(request.POST.get('Rating'))

            UserReviews = Reviews.objects.filter(Profile = _Account).first()
            if UserReviews:
                UserReviews.Content = Content
                UserReviews.Rating = Rating
                UserReviews.save()
            else:
                UserReviews = Reviews.objects.create(Profile = _Account, Content = Content, Rating = Rating)
                UserReviews.save()
            return HttpResponseRedirect(reverse('Public:ReviewsPage'))
        else:
            _Reviews = Reviews.objects.filter(Profile = _Account).first()
            context = {
                "isAuthenticated": True,
                "Account": _Account,
                "Reviews": _Reviews
            }
            return render(request, 'Public/Reviews/ReviewsUpdate.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:ReviewsPage'))