from django.db import models

# Create your models here.

class ScrapedPage(models.Model):
    url = models.TextField()
    title_text = models.TextField()
    title_len = models.IntegerField()
    meta_text = models.TextField()
    meta_len = models.IntegerField()
    h1_text = models.TextField()
    h1_len = models.IntegerField()