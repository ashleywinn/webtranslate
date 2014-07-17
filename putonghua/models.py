from django.db import models

class Sentence(models.Model):
    text = models.TextField(default='')

class EnglishTranslation(models.Model):
    english = models.TextField(unique=True)
    
class ChinesePhrase(models.Model):
    simplified   = models.TextField()
    pinyin       = models.TextField()
    translations = models.ManyToManyField(EnglishTranslation)

class TraditionalToSimplified(models.Model):
    traditional = models.TextField()
    simplified = models.TextField()


