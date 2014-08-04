import re
from putonghua.models import ChineseCharacter, ChinesePhrase, EnglishTranslation

def get_components_of_phrase(simplified):
    max_len = len(simplified)
    if max_len < 1:
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

def get_character_pinyin(simplified):
    # for now grabbing the one with the most english translations
    matches = ChineseCharacter.objects.filter(simplified=simplified)
    pinyin = ''
    trans_cnt = 0
    for char in matches:
        if len(char.translations.all()) > trans_cnt:
            trans_cnt = len(char.translations.all())
            pinyin = char.pinyin
    return pinyin


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

def is_recognized_phrase(simplified):
    if len(get_chinese_phrases(simplified)) > 0:
        return True
    else:
        return False

def find_definitions(simplified):
    length = len(simplified)
    if length == 1:
        matches = ChineseCharacter.objects.filter(simplified=simplified)
    else:
        matches = ChinesePhrase.objects.filter(simplified=simplified)
    for match in matches:
        for trans in match.chinese_english_translations():
            yield trans

def add_character_definition(simplified, traditional, pinyin, english_list):
    try:
        character = ChineseCharacter.objects.get(simplified=simplified, pinyin=pinyin)
    except ChineseCharacter.DoesNotExist:
        character = ChineseCharacter(simplified=simplified, 
                                     traditional=traditional,
                                     pinyin=pinyin)
        character.save()
    for definition in english_list:
        try:
            english_translation = EnglishTranslation.objects.get(english__iexact=definition)
        except EnglishTranslation.DoesNotExist: 
            english_translation = EnglishTranslation(english=definition)
            english_translation.save()
        character.translations.add(english_translation)
    character.save()


def get_chinese_phrases(simplified):
    if (len(simplified) > 1):
        return ChinesePhrase.objects.filter(length=len(simplified), 
                                         simplified=simplified)
    else:
        return ChineseCharacter.objects.filter(simplified=simplified)
        

def add_chinese_phrase(simplified, pinyin=''):
    length = len(simplified)
    try: 
        return ChinesePhrase.objects.get(length=length, simplified=simplified)
    except ChinesePhrase.DoesNotExist:
        phrase = ChinesePhrase(length=length, 
                               simplified=simplified,
                               pinyin=pinyin)
        phrase.save()
        return phrase

def update_phrase_pinyin(phrase, pinyin):
    phrase.pinyin = pinyin
    phrase.save()

def add_english_definition(phrase, english):
    try:
        english_translation = EnglishTranslation.objects.get(english__iexact=english)
    except EnglishTranslation.DoesNotExist: 
        english_translation = EnglishTranslation(english=english)
        english_translation.save()
    phrase.translations.add(english_translation)
    phrase.save()


def add_phrase_definition(simplified, pinyin, english_list):
    phrase = add_chinese_phrase(simplified, pinyin)
    for definition in english_list:
        add_english_definition(phrase, definition)


def load_cedict_file(filename):
    chinese_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+
                                (?P<simplified>[\w・，○]+)\s+
                                \[(?P<pinyin>.*)\]\s+
                                /(?P<english>.*)/""", re.VERBOSE)

    for line in open(filename):
        if line.startswith('#'): continue
        match = chinese_re.match(line)
        if match is None: continue

        traditional = match.group('traditional')
        simplified  = match.group('simplified')
        pinyin      = match.group('pinyin')
        english     = match.group('english')
        definitions = english.split('/')

        if (len(simplified) == 1):
            add_character_definition(simplified, traditional, pinyin, definitions)
        else:
            add_phrase_definition(simplified, pinyin, definitions)
            
