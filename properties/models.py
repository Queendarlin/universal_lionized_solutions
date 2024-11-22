import uuid
from django.db import models


# Enumerations for PropertyType, PropertyStatus, and Currency
class PropertyType(models.TextChoices):
    HOUSE = 'House', 'House'
    LAND = 'Land', 'Land'


class PropertyStatus(models.TextChoices):
    OPEN = 'Open', 'Open'
    INSPECTION_OPEN = 'Inspection Open', 'Inspection Open'
    INSPECTION_CLOSED = 'Inspection Closed', 'Inspection Closed'
    SOLD = 'Sold', 'Sold'


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PropertyType.choices)
    price = models.PositiveIntegerField()  
    square_footage = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PropertyStatus.choices, default=PropertyStatus.OPEN)
    date_closed = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='property_videos/')

    def __str__(self):
        return f"Video for {self.property.title}"