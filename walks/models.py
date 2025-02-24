from django.db import models

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.

class DifficultyLevel(models.Model):
  level = models.CharField(max_length=100)

  def __str__(self):
    return self.level


class Walk(models.Model):
  title = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE,
  related_name="walk_difficulty_level", null=True, blank=True)
  elevation_gain = models.IntegerField()
  distance = models.FloatField(default=0)
  featured_img = models.ImageField(upload_to="static/images/")
  map_img = models.ImageField(upload_to="static/images/", null=True, blank=True)
  content = models.TextField()
  featured = models.BooleanField(default=False)
  status = models.IntegerField(choices=STATUS, default=0)

  def __str__(self):
        return self.title
  
  def content_excerpt(self, char_limit=100):
        if len(self.content) > char_limit:
            return self.content[:char_limit] + '...'
        return self.content