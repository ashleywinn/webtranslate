import re
from django.core import serializers
from putonghua.models import ChineseCharacter, ChinesePhrase, EnglishTranslation
from putonghua.models import Character, CharPinyinEnglish

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

def is_recognized_phrase(simplified):
    if len(get_chinese_phrases(simplified)) > 0:
        return True
    else:
        return False

def find_definitions(simplified):
    length = len(simplified)
    if length == 1:
        matches = Character.objects.filter(char=simplified)
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
        return Character.objects.filter(char=simplified)
        

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

def load_only_characters(simplified, traditional, pinyin, definitions):
    if len(simplified) > 1:
        return
    add_character_with_cedict_definitions(simplified, traditional, pinyin, definitions)

def get_classifiers_from_cedict_definition(definition):
    if not definition.startswith('CL:'):
        return
    definition = definition[3:]
    classifiers = ''
    for desc in definition.split(','):
        m = re.match(r"(?:\w\|)?(\w)", desc)
        classifiers += m.group(1)
    return classifiers

def get_variant_char_from_cedict_definition(definition, traditional=False):
    m = re.search(r"variant of (?:(?P<traditional>\w)\|)(?P<simplified>\w)", 
                  definition)
    if m is not None:
        if traditional and m.group('traditional') is not None:
            return m.group('traditional')
        else:
            return m.group('simplified')
    return ''

    

def add_simplified_character_with_cedict_definitions(simplified, pinyin, definitions,
                                                    alternate_char=''):
    try:
        character = Character.objects.get(char=simplified)
    except Character.DoesNotExist:
        character = Character(char=simplified, 
                              char_type=Character.SIMPLIFIED,
                              pinyin=pinyin)
        character.alternate_char = alternate_char
        character.save()
    for definition in definitions:
        if definition.startswith('CL:'):
            character.classifiers = get_classifiers_from_cedict_definition(definition)
        elif 'variant of' in definition:
            character.variant_of = get_variant_char_from_cedict_definition(definition)
            if character.variant_of == char.char:
                character.variant_of = ''
        else:
            character.add_english_translation_and_pinyin(definition, pinyin)

    character.save()
    return character


def add_traditional_character_with_cedict_definitions(traditional, pinyin, definitions,
                                                     alternate_char=''):
    try:
        character = Character.objects.get(char=traditional)
    except Character.DoesNotExist:
        character = Character(char=traditional, 
                              char_type=Character.TRADITIONAL,
                              pinyin=pinyin)
        character.alternate_char = alternate_char
        character.save()
    for definition in definitions:
        if 'variant of' in definition:
            character.variant_of = get_variant_char_from_cedict_definition(definition, 
                                                                           traditional=True)
            if character.variant_of == char.char:
                character.variant_of = ''
    character.save()
    return character


def add_character_with_cedict_definitions(simplified, traditional, pinyin, definitions):
    if simplified != traditional:
        add_simplified_character_with_cedict_definitions(simplified=simplified, 
                                                        pinyin=pinyin, 
                                                        definitions=definitions,
                                                        alternate_char=traditional)
        add_traditional_character_with_cedict_definitions(traditional=traditional,
                                                         pinyin=pinyin, 
                                                         definitions=definitions,
                                                         alternate_char=simplified)
    else:
        add_simplified_character_with_cedict_definitions(simplified=simplified, 
                                                        pinyin=pinyin, 
                                                        definitions=definitions)


def load_cedict_file(filename, db_update_function):
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

        db_update_function(simplified, traditional, pinyin, definitions)

        # if (len(simplified) == 1):
        #    add_character_definition(simplified, traditional, pinyin, definitions)
        # else:
        #    add_phrase_definition(simplified, pinyin, definitions)
            
