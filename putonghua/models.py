from django.db import models

class Sentence(models.Model):
    text = models.TextField(default='')
