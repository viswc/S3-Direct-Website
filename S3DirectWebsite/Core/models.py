from django.contrib.auth.models import User
from django.db import models
from Authenticate.models import Account
import uuid

class Attachments(models.Model):
    dateCreated = models.DateTimeField(auto_now_add = True)
    dateModified = models.DateTimeField(auto_now = True)
    primaryKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    Profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    File = models.FileField(upload_to='attachments/')
    Type = models.CharField(max_length=100, default="")

class Post(models.Model):
    dateCreated = models.DateTimeField(auto_now_add = True)
    dateModified = models.DateTimeField(auto_now = True)
    primaryKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    Profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100, default="")
    Content = models.CharField(max_length=1000, default="")
    Attachments = models.ManyToManyField(Attachments, blank=True)

    UpvotesCount = models.IntegerField(default=0)
    DownVotesCount = models.IntegerField(default=0)
    CommentsCount = models.IntegerField(default=0)
    Upvotes = models.ManyToManyField(Account, related_name='Upvotes', blank=True)
    Downvotes = models.ManyToManyField(Account, related_name='Downvotes', blank=True)

    isEdited = models.BooleanField(default=False)
    slug = models.CharField(max_length=100, default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super(Post, self).save(*args, **kwargs)

    def generate_slug(self):
        segments = self.Title.split(' ')
        slug = f'{self.Profile.Username.username}-'
        for segment in segments:
            slug += segment.lower() + '-'
        slug += str(self.primaryKey)
        return slug

class Comment(models.Model):
    dateCreated = models.DateTimeField(auto_now_add = True)
    dateModified = models.DateTimeField(auto_now = True)
    primaryKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    Profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Content = models.CharField(max_length=1000, default="")
    Attachments = models.ManyToManyField(Attachments, blank=True)
    isEdited = models.BooleanField(default=False)

class Reviews(models.Model):
    dateCreated = models.DateTimeField(auto_now_add = True)
    dateModified = models.DateTimeField(auto_now = True)
    primaryKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    Profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    Content = models.CharField(max_length=1000, default="")
    Rating = models.IntegerField(default=0)