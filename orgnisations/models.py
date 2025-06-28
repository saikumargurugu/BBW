from django.db import models

# Create your models here.

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#  Create a default organisation when table is created

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not Organisation.objects.exists():
            self.create_default_organisation()



    def create_default_organisation():
        website="http://defaultorganisation.com"
        Organisation.objects.get_or_create(
            name="Default Organisation",
            address="123 Default St, Default City, Default Country",
            phone_number="1234567890",
            email="saikg.dev@gmail.com",
            website=website
        )
