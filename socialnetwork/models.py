from django.db import models
from django.utils import timezone

# django authentication
from django.contrib.auth.models import User

# Create your models here.

class Profiles(models.Model):
    username = models.CharField(max_length=8,primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    age = models.IntegerField(blank=True, null=True)
    bio = models.CharField(blank=True,max_length=430)
    ## Really the url to the picture, left it as picture to require less changes.
    picture = models.CharField(max_length=256, blank=True)
    #image_type = models.CharField(max_length=50, blank=True)

class Posts(models.Model):
    dateTime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profiles)
    content = models.CharField(max_length=160)

class Follow(models.Model):
    user = models.ForeignKey(Profiles, related_name='user')
    following = models.ForeignKey(Profiles, related_name='following')

class Comments(models.Model):
    postID = models.IntegerField()
    dateTime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profiles)
    comment = models.CharField(max_length=160, blank=False, null=False)