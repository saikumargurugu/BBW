from django.db import models
from django.contrib.auth.models import AbstractUser
from orgnisations.models import Organisation



class Users(AbstractUser):
    # Add custom fields here (optional)
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    orgnisations = models.ManyToManyField(Organisation, blank=True) 

    def __str__(self):
        return self.username
