from django.db import models
from django.contrib.auth.models import AbstractUser
from orgnisations.models import Organisation



class Users(AbstractUser):
    """
    Custom user model extending AbstractUser to include additional fields.
    """    
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    orgnisations = models.ManyToManyField(Organisation, blank=True) 
    is_active = models.BooleanField(default=True)
    firebase_uid = models.CharField(max_length=128, blank=True, null=True)  # Store Firebase UID
    date_of_birth = models.DateField(blank=True, null=True)  # Optional field for DOB
    address = models.TextField(blank=True, null=True)  # Optional field for address
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Profile picture


    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the user from Firebase before removing from the database.
        """
        try:
            from firebase_admin import auth
            if self.firebase_uid:  # Ensure Firebase UID exists before attempting deletion
                auth.delete_user(self.firebase_uid)
                print(f"Successfully deleted Firebase user: {self.firebase_uid}")
        except Exception as e:
            print(f"Error deleting Firebase user: {e}")
        super().delete(*args, **kwargs)
