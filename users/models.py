from django.db import models
from django.contrib.auth.models import AbstractUser
from firebase_admin import auth
from orgnisations.models import Organisation


class Router(models.Model):
    url = models.CharField(max_length=255)
    label = models.CharField(max_length=100)
    is_auth_route = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="routers", null=True, blank=True)  # Link to Organisation
    is_global = models.BooleanField(default=False)  # Flag to indicate if the route is global
    sort = models.PositiveIntegerField(default=0)  # Field to control the order of routes

    def __str__(self):
        return f"{self.label} ({self.url})"

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
            if self.firebase_uid:  # Ensure Firebase UID exists before attempting deletion
                auth.delete_user(self.firebase_uid)
                print(f"Successfully deleted Firebase user: {self.firebase_uid}")
        except Exception as e:
            print(f"Error deleting Firebase user: {e}")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.firebase_uid:  # Only create in Firebase if not already created
            try:
                # Create user in Firebase with a temporary password
                print('================================')
                print('File:', "in save method of Users model")
                print('================================')
                firebase_user = auth.create_user(
                    email=self.email,
                    password="temporary_password",  # Set a temporary password
                    display_name=self.username,
                )
                self.firebase_uid = firebase_user.uid  # Save Firebase UID to the database
                print(f"Successfully created Firebase user: {firebase_user.uid}")
            except Exception as e:
                print(f"Error creating Firebase user: {e}")
                raise
        super().save(*args, **kwargs)


class UserAddress(models.Model):
    """
    Model to store user addresses with flags for home and postal addresses.
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_home = models.BooleanField(default=False)  # Flag to indicate if this is the home address
    is_postal = models.BooleanField(default=False)  # Flag to indicate if this is the postal address

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country} ({'Home' if self.is_home else ''}{'Postal' if self.is_postal else ''})"
