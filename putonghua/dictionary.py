import re
import math
import unicodedata
from itertools import zip_longest
from django.core import serializers
from django.db.models import Q, Sum, Max
from putonghua.models import EnglishTranslation
from putonghua.models import ChinesePhrase, ChinesePhraseToEnglish
from putonghua.models import Character, CharPinyinEnglish
from putonghua.models import ChineseWord
from putonghua.models import ChineseHskWord
from putonghua.models import SubtlexCharData, SubtlexWordData
from putonghua.CsvUtil import csv_dict_iter

class ParseError(Exception): pass


def serialize_character_dictionary(outfile):
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    with open(outfile, 'w') as out:
        json_serializer.serialize(list(EnglishTranslation.objects.filter(character__isnull=False)) + 
                                  list(Character.objects.filter(char_type='S')) +  
                                  list(CharPinyinEnglish.objects.filter(character__char_type='S')),
                                  indent=2,
                                  use_natural_primary_keys=True,
                                  use_natural_foreign_keys=True,
                                  stream=out)


def serialize_most_common_characters_and_phrases(phrase_cnt, char_cnt, outfile):
    phrase_score = ChinesePhrase.objects.order_by('-freq_score')[phrase_cnt - 1].freq_score
    char_score = Character.objects.order_by('-freq_score')[char_cnt - 1].freq_score
    serialize_characters_and_phrases_with_freq(phrase_score, char_score, outfile)

def serialize_characters_and_phrases_with_freq(phrase_score, char_score, outfile):
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()

    character_set      = Character.objects.filter(freq_score__gte=char_score)
    char_connect_set   = CharPinyinEnglish.objects.filter(
                                     character__freq_score__gte=char_score)
    phrase_set         = ChinesePhrase.objects.filter(freq_score__gte=phrase_score)
    phrase_connect_set = ChinesePhraseToEnglish.objects.filter(
                                     phrase__freq_score__gte=phrase_score)
    english_set = EnglishTranslation.objects.annotate(
                          phrase_score=Max('chinesephrase__freq_score')).annotate(
                            char_score=Max('character__freq_score')).filter(
                          (Q(phrase_score__isnull=False) & Q(phrase_score__gte=phrase_score)) |
                          (Q(char_score__isnull=False) & Q(char_score__gte=char_score))).distinct()

    with open(outfile, 'w') as out:
        json_serializer.serialize(list(english_set) +
                                  list(character_set) + list(char_connect_set) +
                                  list(phrase_set) + list(phrase_connect_set),
                                  indent=2,
                                  use_natural_primary_keys=True,
                                  use_natural_foreign_keys=True,
                                  stream=out)

def upload_hsk_list_file(hsk_list_file, list_number):
    list_number = int(list_number)
    no_break_char = unicodedata.lookup("ZERO WIDTH NO-BREAK SPACE")
    for line in open(hsk_list_file):
        try:
            (simplified, traditional, 
             pinyin, pinyin2, definitions) = line.split('\t', maxsplit=4)
        except ValueError:
            continue
        simplified = simplified.strip().replace(no_break_char, '')
        definitions = [define.strip() for define in definitions.split(';')]
        pinyin = pinyin.split(',', 2)[0]
        pinyin = re.sub(r"([0-5])", r"\1 ", pinyin).strip()
        add_hsk_word(list_number, simplified, pinyin, definitions)


def add_hsk_word(hsk_list, simplified, pinyin, definitions):
    try:
        chineseword = ChineseWord.objects.get_simplified_exact(
                                                       simplified=simplified)
    except ChineseWord.DoesNotExist:
        chineseword = add_chinese_word(simplified, pinyin)

    hsk_word, created = ChineseHskWord.objects.get_or_create(
                                               chineseword=chineseword,
                                               defaults={'hsk_list': hsk_list})
    for i, definition in enumerate(definitions):
        hsk_word.add_definition(pinyin, definition, i + 1)
    return hsk_word


def add_chinese_word(simplified, pinyin, definitions=[], ranks=[]):
    character = None
    phrase = None
    if len(simplified) == 1:
        try:
            character = Character.objects.get(char=simplified)
        except Character.DoesNotExist:
            character = Character.objects.create(char=simplified, 
                                                 char_type=Character.SIMPLIFIED,
                                                 pinyin=pinyin)
    else:
        try:
            phrase = ChinesePhrase.objects.get(simplified=simplified)
        except ChinesePhrase.DoesNotExist:
            phrase = ChinesePhrase.objects.create(simplified=simplified, 
                                                  pinyin=pinyin)
    
    word, created = ChineseWord.objects.get_or_create(character=character,
                                                      phrase=phrase)
    assert(len(definitions) >= len(ranks))
    for definition, rank in zip_longest(definitions, ranks, fillvalue=0):
        word.add_definition(definition, pinyin, rank)
    return word



def update_char_pinyin_from_hsk():
    for char in Character.objects.filter(chinesehskword__isnull=False):
        hsk_pinyin = char.chinesehskword.hskwordtoenglish_set.first().pinyin
        hsk_pinyin_list = [pinyin.strip() for pinyin in hsk_pinyin.split(',')]
        if len(hsk_pinyin_list) > 1:
            if char.pinyin not in hsk_pinyin_list:
                print("%s : %s -> %s" % (char.char, char.pinyin, hsk_pinyin))


def get_recognized_components(text, recognizer, max_len=100):
    while len(text) > 1:
        for i in range(len(text), 0, -1):
            if i >= max_len: continue
            if i == 1:
                yield text[0]
                text = text[1:]
                break
            if recognizer(text[0:i]):
                yield text[0:i]
                text = text[i:]
                break
    if len(text):
        yield text


def get_toneless_pinyin_components(pinyin):
    for pinyin_word in pinyin.split():
        yield from get_recognized_components(pinyin_word, is_recognized_toneless_pinyin, 
                                             max_len=25)

def is_recognized_toneless_pinyin(pinyin):
    if ChinesePhrase.objects.filter_tonelesspinyin_exact(pinyin).exists():
        return True
    if Character.objects.filter_tonelesspinyin_exact(pinyin).exists():
        return True
    return False


# def get_components_of_phrase(simplified, max_len=100):
#    yield from get_recognized_components(simplified, is_recognized_phrase,
#                                         max_len=max_len)

def get_components_of_phrase(simplified):
    max_len = len(simplified)
    if max_len <= 1:
        return simplified
    while len(simplified) > 1:
        for i in range(len(simplified), 0, -1):
            if i >= max_len: continue
            if i == 1:
                yield simplified[0]
                simplified = simplified[1:]
                break
            if is_recognized_phrase(simplified[0:i]):
                yield simplified[0:i]
                simplified = simplified[i:]
                break
    if len(simplified):
        yield simplified


def is_recognized_phrase(simplified):
    if ChinesePhrase.objects.filter(simplified=simplified).exists():
        return True
    else:
        return False


def get_character_pinyin(simplified):
    # for now this is just the first pinyin found for a character
    try:
        return Character.objects.get(char=simplified).pinyin
    except Character.DoesNotExist:
        return '?'

def get_phrase_pinyin(simplified):
    try:
        phrase = ChinesePhrase.objects.get(simplified=simplified)
        if len(phrase.pinyin) > 0:
            return phrase.pinyin
    except ChinesePhrase.DoesNotExist:
        pass
    pinyin = ''
    for char in simplified:
        pinyin = '{} {}'.format(pinyin, get_character_pinyin(char))
    return pinyin.strip()

def find_definitions(simplified):
    length = len(simplified)
    if length == 1:
        matches = Character.objects.filter(char=simplified).order_by('-freq_score')
    else:
        matches = ChinesePhrase.objects.filter(simplified=simplified).order_by('-freq_score')
    for match in matches:
        yield from match.compact_english_translations(definition_cnt=3)


def add_english_definition(phrase, english, rank=0):
    try:
        english_translation = EnglishTranslation.objects.get(english__iexact=english)
    except EnglishTranslation.DoesNotExist: 
        english_translation = EnglishTranslation(english=english)
        english_translation.save()
    try:
        connect = ChinesePhraseToEnglish.objects.get(englishtranslation=english_translation,
                                                     phrase=phrase)
        if (rank != connect.rank):
            connect.rank = rank
            connect.save()
    except ChinesePhraseToEnglish.DoesNotExist: 
        connect = ChinesePhraseToEnglish(englishtranslation=english_translation,
                                         phrase=phrase,
                                         rank=rank)
        connect.save()


    
    
