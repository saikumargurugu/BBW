import uuid
from django.db import models

# Create your models here.

class Uploads(models.Model):
    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    path = models.CharField(max_length=500)
    model = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=50) 

    class Meta:
        db_table = 'uploads'

    def __str__(self):
        return f"{self.model} - {self.path} ({self.file_size} bytes, {self.type})"
