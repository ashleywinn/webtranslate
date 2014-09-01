import re
from putonghua.models import Character, ChinesePhrase
from putonghua.models import ChineseWord, ChineseName
from putonghua.models import EnglishTranslation


class ParseError(Exception): pass


def upload_cedict_file(filename):
    for (simplified, 
         traditional, 
         pinyin,
         definitions) in parse_cedict_file(filename):

        if len(simplified) > 1:
            load_cedict_chinese_phrase(simplified, 
                                       pinyin, definitions)
        else:
            load_cedict_chinese_character(simplified, traditional, 
                                          pinyin, definitions)
            

def parse_cedict_file(filename):
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

        yield (simplified, traditional, pinyin, definitions)

def fix_cedict_classifier_definitions():
    for cl_def in EnglishTranslation.objects.filter(english__startswith='CL:'):
        classifiers = get_classifiers_from_cedict_definition(cl_def.english)
        for phr in cl_def.chinesephrase_set.all():
            handle_cedict_phrase_word(phr, classifiers)
        cl_def.chinesephrasetoenglish_set.all().delete()
        for char in cl_def.character_set.all():
            handle_cedict_character_word(char, classifiers)
        cl_def.charpinyinenglish_set.all().delete()
    EnglishTranslation.objects.filter(english__startswith='CL:').delete()

def change_character_classifiers_to_word_classifiers():
    for char in Character.objects.exclude(classifiers=''):
        handle_cedict_character_word(char, char.classifiers)


def load_cedict_chinese_phrase(simplified, pinyin, definitions):
    try:
        phrase = ChinesePhrase.objects.get(simplified=simplified)
    except ChinesePhrase.DoesNotExist:
        phrase = ChinesePhrase(simplified=simplified, 
                               pinyin=pinyin.casefold())
        phrase.save()

    # Is it a name?
    if not pinyin.islower():
        handle_cedict_phrase_name(phrase, pinyin, definitions)
        return

    for definition in definitions:
        if definition.startswith('CL:'):
            classifiers = get_classifiers_from_cedict_definition(definition)
            if not len(classifiers): raise ParseError()
            handle_cedict_phrase_word(phrase, classifiers)
        elif 'variant of' in definition:
            phrase.variant_of = get_variant_from_cedict_definition(definition)
            if phrase.variant_of == phrase.simplified:
                phrase.variant_of = ''
        else:
            phrase.add_definition(definition)

    phrase.save()
    return phrase


def handle_cedict_phrase_name(phrase, pinyin, definitions):
    try:
        name = ChineseName.objects.get(phrase=phrase)
    except ChineseName.DoesNotExist:
        name = ChineseName(phrase=phrase,
                           pinyin=pinyin)
        name.save()
    for defined in definitions:
        name.add_definition(defined)

    
def handle_cedict_character_name(character, pinyin, definitions):
    try:
        name = ChineseName.objects.get(character=character)
    except ChineseName.DoesNotExist:
        name = ChineseName(character=character,
                           pinyin=pinyin)
        name.save()
    for defined in definitions:
        name.add_definition(defined)

    
def handle_cedict_phrase_word(phrase, classifiers):
    try:
        word = ChineseWord.objects.get(phrase=phrase)
        for cl_char in classifiers:
            word.add_classifier(cl_char)
        word.save()
    except ChineseWord.DoesNotExist:
        word = ChineseWord(phrase=phrase,
                           classifiers=classifiers)
        word.save()
    

def handle_cedict_character_word(character, classifiers):
    try:
        word = ChineseWord.objects.get(character=character)
        for cl_char in classifiers:
            word.add_classifier(cl_char)
        word.save()
    except ChineseWord.DoesNotExist:
        word = ChineseWord(character=character,
                           classifiers=classifiers)
        word.save()


def get_classifiers_from_cedict_definition(definition):
    if not definition.startswith('CL:'):
        return
    definition = definition[3:]
    classifiers = ''
    for desc in definition.split(','):
        m = re.match(r"\s*(?:\w\|)?(\w)", desc)
        if m is None:
            raise ParseError("no classifiers found: {} -> {}".format(definition, desc))
        classifiers += str(m.group(1))
    return classifiers


def get_variant_from_cedict_definition(definition, traditional=False):
    m = re.search(r"variant of (?:(?P<traditional>\w+)\|)(?P<simplified>\w+)", 
                  definition)
    if m is not None:
        if traditional and m.group('traditional') is not None:
            return m.group('traditional')
        else:
            return m.group('simplified')
    return ''


def load_cedict_chinese_character(simplified, traditional, pinyin, definitions):
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


def add_simplified_character_with_cedict_definitions(simplified, pinyin, definitions,
                                                    alternate_char=''):
    try:
        character = Character.objects.get(char=simplified)
    except Character.DoesNotExist:
        character = Character(char=simplified, 
                              char_type=Character.SIMPLIFIED,
                              pinyin=pinyin.casefold())
        character.alternate_char = alternate_char
        character.save()

    # Is it a name?
    if not pinyin.islower():
        handle_cedict_character_name(character, pinyin, definitions)
        return

    for definition in definitions:
        if definition.startswith('CL:'):
            classifiers = get_classifiers_from_cedict_definition(definition)
            if len(classifiers) == 0: raise ParseError()
            handle_cedict_character_word(character, classifiers)
        elif 'variant of' in definition:
            character.variant_of = get_variant_from_cedict_definition(definition)
            if character.variant_of == character.char:
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
            character.variant_of = get_variant_from_cedict_definition(definition, 
                                                                      traditional=True)
            if character.variant_of == character.char:
                character.variant_of = ''
    character.save()
    return character

