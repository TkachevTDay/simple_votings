from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class Voting(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)

    """
    0 - discrete
    1 - 1:N
    2 - M:N 
    """
    open = models.BooleanField(default=1)  # если закрыто - 0, иначе - 1
    type = models.IntegerField(default=0)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)


class VoteVariant(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)


class VoteFact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
