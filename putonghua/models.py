from django.db import models
from hashlib import md5

class ChineseEnglishTranslation(object):
    def __init__(self, simplified='', pinyin='', english=''):
        self.simplified = simplified
        self.pinyin = pinyin
        self.english = english

class Sentence(models.Model):
    text = models.TextField(default='')

class EnglishTranslationManager(models.Manager):
    def get_by_natural_key(self, eng_md5):
        return self.get(eng_md5=eng_md5)

class EnglishTranslation(models.Model):
    objects = EnglishTranslationManager();

    english = models.TextField()
    eng_md5 = models.CharField(max_length=32)

    def update_md5(self):
        self.eng_md5 = md5(self.english.encode()).hexdigest()
        self.save()

    def natural_key(self):
        return (self.eng_md5,)


class Character(models.Model):
    SIMPLIFIED  = 'S'
    TRADITIONAL = 'T'
    CHAR_TYPES  = ((SIMPLIFIED,  'Simplified'),
                   (TRADITIONAL, 'Traditional'),
                   )
    char           = models.CharField(max_length=1, primary_key=True)
    char_type      = models.CharField(max_length=1,
                                      choices=CHAR_TYPES)
    pinyin         = models.CharField(max_length=16)
    classifiers    = models.CharField(max_length=8, blank=True)
    alternate_char = models.CharField(max_length=1, blank=True)
    variant_of     = models.CharField(max_length=1, blank=True)
    composed_of    = models.CharField(max_length=8, blank=True)
    translations   = models.ManyToManyField(EnglishTranslation,
                                            through='CharPinyinEnglish')

    def add_english_translation_and_pinyin(self, english_def, pinyin):
        try:
            return self.translations.get(english__iexact=english_def)
        except EnglishTranslation.DoesNotExist:
            pass
        english_trans = None
        try: 
            english_trans = EnglishTranslation.objects.get(english__iexact=english_def)
        except EnglishTranslation.DoesNotExist:
            english_trans = EnglishTranslation(english=english_def)
            english_trans.save()
        cpe = CharPinyinEnglish(englishtranslation=english_trans,
                                character=self,
                                pinyin=pinyin)
        cpe.save()
        return english_trans

    def english_list(self):
        for translation in self.translations.all():
            yield translation.english

    def pinyin_and_english_list(self):
        for translation in self.translations.all():
            connect = CharPinyinEnglish.objects.get(character=self,
                                                    englishtranslation=translation)
            yield (connect.pinyin, translation.english)

    def chinese_english_translations(self):
        for pinyin, english in self.pinyin_and_english_list():
            yield ChineseEnglishTranslation(simplified=self.char,
                                            pinyin=pinyin,
                                            english=english)





class CharPinyinEnglishManager(models.Manager):
    def get_by_natural_key(self, englishtranslation, character):
        return self.get(englishtranslation=englishtranslation, character=character)
    
class CharPinyinEnglish(models.Model):
    objects = CharPinyinEnglishManager();

    englishtranslation = models.ForeignKey(EnglishTranslation)
    character          = models.ForeignKey(Character)
    pinyin             = models.CharField(max_length=16)

    def natural_key(self):
        return (self.englishtranslation, self.character)

    
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


