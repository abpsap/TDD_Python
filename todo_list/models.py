from django.db import models

# Create your models here.
class Profile(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    profile = models.ForeignKey(Profile, default=None)
