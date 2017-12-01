from django.db import models

from interceptee import Interceptee

class Story(models.Model):
    interceptee = models.ForeignKey(Interceptee)
    story = models.CharField(max_length=4096, blank=True)