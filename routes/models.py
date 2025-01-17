from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Route(models.Model):
    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_routes")
    date = models.DateField()
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance = models.FloatField(null=True, blank=True)
    elevation = models.FloatField(null=True, blank=True)
    time_taken = models.FloatField(null=True, blank=True)
    route_img = CloudinaryField('image', null=True, blank=True )
    comments = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    @staticmethod
    def total_distance():
        return Route.objects.aggregate(total_distance=Sum('distance'))['total_distance'] or 0
    
    @staticmethod
    def total_elevation():
        return Route.objects.aggregate(total_elevation=Sum('elevation'))['total_elevation'] or 0
