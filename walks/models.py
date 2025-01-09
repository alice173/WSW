from django.db import models

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.

class Walk(models.Model):
  title = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  map_img = models.ImageField(upload_to="static/images/")
  content = models.TextField()
  status = models.IntegerField(choices=STATUS, default=0)