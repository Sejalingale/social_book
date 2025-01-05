# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.CharField(max_length=50, choices=[('public', 'Public'), ('private', 'Private')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_of_publication = models.IntegerField()
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
