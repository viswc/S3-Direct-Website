from django.contrib.auth.models import User
from django.db import models
import uuid

class Account(models.Model):
    dateCreated = models.DateTimeField(auto_now_add = True)
    dateModified = models.DateTimeField(auto_now = True)
    primaryKey = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    Username = models.OneToOneField(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    email = models.CharField(max_length=100, default="")
    firstName = models.CharField(max_length=100, default="")
    lastName = models.CharField(max_length=100, default="")