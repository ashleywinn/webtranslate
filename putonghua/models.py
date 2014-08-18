from django.db import models
from hashlib import md5

def hashtext(txt):
    return md5(txt.casefold().encode()).hexdigest()

def get_create_EnglishTranslation(english):
    english_hash = hashtext(english)
    try: 
        return EnglishTranslation.objects.get(eng_md5=english_hash)
    except EnglishTranslation.DoesNotExist:
        return EnglishTranslation.objects.create(english=english)
    

class ChineseEnglishTranslation(object):
    def __init__(self, simplified='', pinyin='', english=''):
        self.simplified = simplified
        self.pinyin = pinyin
        self.english = english

class EnglishTranslationManager(models.Manager):
    def get_by_natural_key(self, eng_md5):
        return self.get(eng_md5=eng_md5)

class EnglishTranslation(models.Model):
    objects = EnglishTranslationManager();

    english = models.TextField()
    eng_md5 = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        self.eng_md5 = hashtext(self.english)
        super(EnglishTranslation, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.eng_md5,)


class Character(models.Model):
    SIMPLIFIED  = 'S'
    TRADITIONAL = 'T'
    CHAR_TYPES  = ((SIMPLIFIED,  'Simplified'),
                   (TRADITIONAL, 'Traditional'))

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
    freq_score   = models.PositiveSmallIntegerField(default=0)  # (0-999) log1p(x / 50000)

    def add_english_translation_and_pinyin(self, english, pinyin,
                                           rank=0):
        try:
            connect = self.translations.get(eng_md5=hashtext(english))
            connect.rank = rank
            connect.save()
            return
        except EnglishTranslation.DoesNotExist: 
            pass
        translation = get_create_EnglishTranslation(english)
        CharPinyinEnglish.objects.create(englishtranslation=translation,
                                         character=self,
                                         pinyin=pinyin,
                                         rank=rank)

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

    def add_radical_component(self, radical_char):
        if radical_char not in self.composed_of:
            self.composed_of = self.composed_of + str(radical_char)
            self.save()

    def radical_components(self):
        for rad in self.composed_of:
            yield rad



class CharPinyinEnglishManager(models.Manager):
    def get_by_natural_key(self, englishtranslation, character):
        return self.get(englishtranslation=englishtranslation, character=character)
    
class CharPinyinEnglish(models.Model):
    objects = CharPinyinEnglishManager();

    englishtranslation = models.ForeignKey(EnglishTranslation)
    character          = models.ForeignKey(Character)
    pinyin             = models.CharField(max_length=16)
    rank               = models.PositiveSmallIntegerField()

    def natural_key(self):
        return (self.englishtranslation, self.character)


class ChinesePhraseManager(models.Manager):
    def get_by_natural_key(self, phrase_md5):
        return self.get(phrase_md5=phrase_md5)

class ChinesePhrase(models.Model):
    objects = ChinesePhraseManager()

    length       = models.SmallIntegerField()
    simplified   = models.TextField()
    phrase_md5   = models.CharField(max_length=32)
    pinyin       = models.TextField()
    definitions  = models.ManyToManyField(EnglishTranslation,
                                          through='ChinesePhraseToEnglish')
    freq_score   = models.PositiveSmallIntegerField(default=0)  # (0-999) log1p(x / 50000)


    def update_md5(self):
        self.phrase_md5 = hashtext(self.simplified)
        self.save()

    # def save(self, *args, **kwargs):
        # self.length = len(self.simplified)
        # self.phrase_md5 = hashtext(self.simplified)
        # super(ChinesePhrase, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.phrase_md5,)

    def english_list(self):
        for definition in self.definitions.all():
            yield definition.english

    def chinese_english_translations(self):
        for english in self.english_list():
            yield ChineseEnglishTranslation(simplified=self.simplified,
                                            pinyin=self.pinyin,
                                            english=english)

    def get_definition_rank(self, english):
        self.chinesephrasetoenglish_set.get(
            englishtranslation__eng_md5=hashtext(english)).rank

    def set_definition_rank(self, english, rank):
        connect = self.chinesephrasetoenglish_set.get(
            englishtranslation__eng_md5=hashtext(english))
        connect.rank = rank
        connect.save()

    def add_definition(self, english, rank=0):
        try: 
            definition = self.definitions.get(eng_md5=hashtext(english))
            if rank != 0:
                self.set_definition_rank(english, rank)
            return
        except EnglishTranslation.DoesNotExist:
            pass
        definition = get_create_EnglishTranslation(english)
        ChinesePhraseToEnglish.objects.create(englishtranslation=definition,
                                              phrase=self,
                                              rank=rank)


class ChinesePhraseToEnglishManager(models.Manager):
    def get_by_natural_key(self, englishtranslation, phrase):
        return self.get(englishtranslation=englishtranslation, phrase=phrase)
    
class ChinesePhraseToEnglish(models.Model):
    objects = ChinesePhraseToEnglishManager();

    englishtranslation = models.ForeignKey(EnglishTranslation)
    phrase             = models.ForeignKey(ChinesePhrase)
    rank               = models.PositiveSmallIntegerField()

    def natural_key(self):
        return (self.englishtranslation, self.phrase)


class SubtlexCharData(models.Model):
    character  = models.OneToOneField(Character)
    count      = models.PositiveIntegerField()

class SubtlexWordData(models.Model):
    phrase     = models.OneToOneField(ChinesePhrase)
    count      = models.PositiveIntegerField()


class ChineseHskWord(models.Model):
    hsk_list     = models.PositiveSmallIntegerField()
    character    = models.OneToOneField(Character, null=True)
    phrase       = models.OneToOneField(ChinesePhrase, null=True)
    definitions  = models.ManyToManyField(EnglishTranslation,
                                          through='HskWordToEnglish')
    
    def add_definition(self, pinyin, english, rank):
        try: 
            self.definitions.get(eng_md5=hashtext(english))
            return
        except EnglishTranslation.DoesNotExist:
            pass
        definition = get_create_EnglishTranslation(english)
        HskWordToEnglish.objects.create(englishtranslation=definition,
                                        chinesehskword=self,
                                        pinyin=pinyin,
                                        rank=rank)

class HskWordToEnglish(models.Model):
    englishtranslation = models.ForeignKey(EnglishTranslation)
    chinesehskword     = models.ForeignKey(ChineseHskWord)
    pinyin             = models.CharField(max_length=32)
    rank               = models.PositiveSmallIntegerField()


