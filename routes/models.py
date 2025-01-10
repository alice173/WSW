from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Route(models.Model):
    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_routes")
    date = models.DateField()
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance = models.FloatField()
    elevation = models.FloatField()
    time_taken = models.TimeField()
    route_img = models.ImageField(upload_to="static/images/")
    comments = models.TextField()

    def __str__(self):
        return self.title
