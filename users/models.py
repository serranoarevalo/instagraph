from django.db import models
from django.contrib.auth.models import AbstractUser


class DateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, DateModel):

    name = models.CharField(max_length=250)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username
