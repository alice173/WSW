from django.db import models

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.

class DifficultyLevel(models.Model):
  level = models.CharField(max_length=100)
  walk = models.ForeignKey(
        'Walk', on_delete=models.CASCADE, related_name="walk_difficulty_level")


class Walk(models.Model):
  title = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE,
  related_name="walk_difficulty_level", null=True, blank=True)
  elevation_gain = models.IntegerField()
  map_img = models.ImageField(upload_to="static/images/")
  content = models.TextField()
  status = models.IntegerField(choices=STATUS, default=0)