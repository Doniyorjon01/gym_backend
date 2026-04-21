import base64
from uuid import uuid4

from django.core.files.base import ContentFile

from accounts.models import BaseData, User
from django.db import models

class SportType(BaseData):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(BaseData):
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.address


class Gym(BaseData):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='gyms')
    open_time = models.TimeField()
    close_time = models.TimeField()
    owner = models.ForeignKey(User, related_name='owned_gyms', on_delete=models.CASCADE)
    trainers = models.ManyToManyField(User, related_name='training_gyms', blank=True)
    image_file = models.ImageField(upload_to='gym/', blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    three_month_discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    six_month_discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    twelve_month_discount_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name or ''


    def save(self, *args, **kwargs):
        if self.image and len(self.image) > 101:
            try:
                img_data = base64.b64decode(str(self.image))
                filename = f"{uuid4()}"
                self.image_file.save(filename, ContentFile(img_data), save=False)
                self.image = filename
            except Exception as e:
                raise ValueError(f"Invalid base64 image format: {e}")

        return super().save(*args, **kwargs)