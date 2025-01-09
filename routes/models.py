from django.db import models

# Create your models here.

class Route(models.Model):
    title = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance = models.FloatField()
    elevation = models.FloatField()
    time_taken = models.TimeField()
    route_img = models.ImageField(upload_to="static/images/")
    comments = models.TextField()
   