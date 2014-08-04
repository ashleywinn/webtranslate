from django.db import models

class ChineseEnglishTranslation(object):
    def __init__(self, simplified='', pinyin='', english=''):
        self.simplified = simplified
        self.pinyin = pinyin
        self.english = english

class Sentence(models.Model):
    text = models.TextField(default='')

class EnglishTranslation(models.Model):
    english = models.TextField()
    
class ChineseCharacter(models.Model):
    simplified   = models.CharField(max_length=1)
    traditional  = models.CharField(max_length=1)
    pinyin       = models.CharField(max_length=16)
    translations = models.ManyToManyField(EnglishTranslation)

    def english_list(self):
        for translation in self.translations.all():
            yield translation.english

    def chinese_english_translations(self):
        for english in self.english_list():
            yield ChineseEnglishTranslation(simplified=self.simplified,
                                            pinyin=self.pinyin,
                                            english=english)


class ChinesePhrase(models.Model):
    length       = models.SmallIntegerField()
    simplified   = models.TextField()
    pinyin       = models.TextField()
    translations = models.ManyToManyField(EnglishTranslation)

    def english_list(self):
        for translation in self.translations.all():
            yield translation.english

    def chinese_english_translations(self):
        for english in self.english_list():
            yield ChineseEnglishTranslation(simplified=self.simplified,
                                            pinyin=self.pinyin,
                                            english=english)


