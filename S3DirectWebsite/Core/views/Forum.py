from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Authenticate.models import *
from Core.models import *

def forum(request):
    if request.method == 'GET':
        sortby = request.GET.get('sortby')
        if sortby == 'ascdate':
            sortby = 'dateCreated'
        elif sortby == 'dscdate':
            sortby = '-dateCreated'
        elif sortby == 'mcomments':
            sortby = '-CommentsCount'
        elif sortby == 'mliked':
            sortby = '-UpvotesCount'
        else:
            sortby = '-dateCreated'

        Forums = Post.objects.filter().order_by(sortby)
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)
            context = {
                "isAuthenticated": True,
                "Account": _Account,
                "Forums": Forums
            }
        else:
            context = {
                "isAuthenticated": False,
                "Forums": Forums
            }
        return render(request, 'Public/Forum/Forum.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
    
def forumCreate(request):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        if request.method == 'POST':
            Title = request.POST.get('Title')
            Content = request.POST.get('Content')
            _Attachments = request.FILES.getlist('Attachments')
            
            _Post = Post.objects.create(Profile = _Account, Title = Title, Content = Content)
            Segments, Slug = Title.split(' '), f'{_Account.Username}-'
            for Segment in Segments:
                Slug += Segment.lower() + '-'
            Slug += str(_Post.primaryKey)
            _Post.slug = Slug
            _Post.save()

            for attachment in _Attachments:
                _Attachment = Attachments.objects.create(Profile = _Account, Image = attachment)
                _Post.Attachments.add(_Attachment)
                _Post.save()
            return HttpResponseRedirect(reverse('Public:ForumPage'))
        else:
            context = {
                "isAuthenticated": True,
                "Account": _Account
            }
            return render(request, 'Public/Forum/ForumCreate.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
        
def forumDetail(request, slug):
    if request.method == 'GET':
        _Post = Post.objects.get(slug = slug)
        if request.user.is_authenticated:
            _Account = Account.objects.get(Username = request.user)

            userComment = Comment.objects.filter(Profile = _Account, Post = _Post).first()
            Commented = Comment.objects.filter(Profile = _Account, Post = _Post).exists()
            Liked = _Post.Upvotes.filter(Username = _Account.Username).exists()
            Disliked = _Post.Downvotes.filter(Username = _Account.Username).exists()
            Comments = Comment.objects.filter(Post = _Post).exclude(Profile = _Account).order_by('-dateCreated')

            context = {
                "isAuthenticated": True,
                "Account": _Account,
                "Post": _Post,
                "Comments": Comments,
                "UserComment": userComment,
                "Commented": Commented,
                "Liked": Liked,
                "Disliked": Disliked,
            }
        else: 
            Comments = Comment.objects.filter(Post = _Post).order_by('-dateCreated')
            context = {
                "isAuthenticated": False,
                "Post": _Post,
                "Comments": Comments
            }
        return render(request, 'Public/Forum/ForumDetail.html', context)
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
    
def forumComment(request, slug):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        _Post = Post.objects.get(slug = slug)
        if request.method == 'POST':
            Content = request.POST.get('Content')
            _Attachments = request.FILES.getlist('Attachments')

            if Comment.objects.filter(Profile = _Account, Post = _Post).exists():
                Comment.objects.filter(Profile = _Account, Post = _Post).delete()
                _Post.CommentsCount -= 1
                _Post.save()
            
            _Comment = Comment.objects.create(Profile = _Account, Post = _Post, Content = Content)
            for attachment in _Attachments:
                _Attachment = Attachments.objects.create(Profile = _Account, Image = attachment)
                _Comment.Attachments.add(_Attachment)
                _Comment.save()
            _Post.CommentsCount += 1
            _Post.save()
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
        else:
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
    
def forumEdit(request, slug):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        _Post = Post.objects.get(slug = slug)
        if request.method == 'POST' and _Post.Profile.Username == _Account.Username:
            Title = request.POST.get('Title')
            Content = request.POST.get('Content')
            _Attachments = request.FILES.getlist('Attachments')
            
            _Post.Title = Title
            _Post.Content = Content
            _Post.Attachments.clear()
            _Post.save()

            for attachment in _Attachments:
                _Attachment = Attachments.objects.create(Profile = _Account, Image = attachment)
                _Post.Attachments.add(_Attachment)
                _Post.save()
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
        else:
            if _Post.Profile.Username == _Account.Username:
                context = {
                    "isAuthenticated": True,
                    "Account": _Account,
                    "Post": _Post
                }
                return render(request, 'Public/Forum/ForumEdit.html', context)
            else:
                return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
    
def forumAction(request, slug):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        _Post = Post.objects.get(slug = slug)
        if request.method == 'POST':
            Action = request.POST.get('Action')
            if Action == 'Upvote':
                if _Post.Downvotes.filter(Username = _Account.Username).exists():
                    _Post.Downvotes.remove(_Account)
                    _Post.DownVotesCount -= 1
                    _Post.save()

                if _Post.Upvotes.filter(Username = _Account.Username).exists():
                    _Post.Upvotes.remove(_Account)
                    _Post.UpvotesCount -= 1
                    _Post.save()
                else:
                    _Post.Upvotes.add(_Account)
                    _Post.UpvotesCount += 1
                    _Post.save()
            elif Action == 'Downvote':
                if _Post.Upvotes.filter(Username = _Account.Username).exists():
                    _Post.Upvotes.remove(_Account)
                    _Post.UpvotesCount -= 1
                    _Post.save()

                if _Post.Downvotes.filter(Username = _Account.Username).exists():
                    _Post.Downvotes.remove(_Account)
                    _Post.DownVotesCount -= 1
                    _Post.save()
                else:
                    _Post.Downvotes.add(_Account)
                    _Post.DownVotesCount += 1
                    _Post.save()
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
        else:
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))
    
def forumDelete(request, slug):
    if request.user.is_authenticated:
        _Account = Account.objects.get(Username = request.user)
        _Post = Post.objects.get(slug = slug)
        if request.method == 'POST':
            if _Post.Profile.Username == _Account.Username:
                _Post.delete()
            return HttpResponseRedirect(reverse('Public:ForumPage'))
        else:
            return HttpResponseRedirect(reverse('Public:ForumDetailPage', args = [slug]))
    else:
        return HttpResponseRedirect(reverse('Public:ForumPage'))