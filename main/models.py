from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class VoteFact(models.Model):
    user = models.IntegerField()
    variant = models.IntegerField()
    created_at = models.DateTimeField()


class VoteVariant(models.Model):
    voting = models.IntegerField()
    description = models.CharField(max_length=60)


class Voting(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=60)
    type = models.IntegerField()
    author = models.IntegerField()
