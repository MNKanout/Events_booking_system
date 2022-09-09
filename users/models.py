from django.db import models
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):
    username = models.CharField(('username'),
    max_length=12,
    unique=True,
    help_text=('+47 xx-xxx-xxx'),
    error_messages={
        'unique': ("A user with that phone number already exists."),
    },)
    email = models.EmailField(unique=True,blank=False)
    birthday = models.DateField(blank=True, null=True)

    


    def __str__(self):
        return self.username
