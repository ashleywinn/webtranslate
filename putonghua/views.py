from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from putonghua.models import Character, ChinesePhrase, ChineseWord, ChineseName
from putonghua.models import ChineseEnglishTranslation, ChineseHskWord
from putonghua.dictionary import find_definitions, add_chinese_phrase
from putonghua.dictionary import add_english_definition, get_components_of_phrase
from putonghua.dictionary import get_phrase_pinyin, update_phrase_pinyin


def find_first_definition(phrase):
    for definition in find_definitions(phrase):
        return definition
    return None

def find_up_to_n_definitions(n, phrase):
    for idx, definition in enumerate(find_definitions(phrase)):
        yield definition
        if idx > (n - 2): break

def get_definitions(chin_str):
    yield from find_definitions(chin_str)
    if len(chin_str) > 1:
        for component in get_components_of_phrase(chin_str):
            yield from find_up_to_n_definitions(4, component)

def hsk_word_list_translations(list_number):
    return [hsk.compact_english_translation(definition_cnt=3)
            for hsk in ChineseHskWord.objects.filter(hsk_list=list_number)]


def home_page(request):
    return render(request, 'home.html')

def new_chinese(request):
    new_phrase_text = request.POST.get('new_phrase', '').strip()
    if new_phrase_text == '':
        return redirect('/')
    return redirect('/putonghua/{}/english/'.format(new_phrase_text))

def new_translation(request, chinese_phrase):
    english_text = request.POST.get('english', '').strip()
    if english_text != '':
        phrase = add_chinese_phrase(chinese_phrase)
        add_english_definition(phrase, english_text)
        if not phrase.pinyin:
            phrase.pinyin = get_phrase_pinyin(chinese_phrase)
            phrase.save()
    return redirect('/putonghua/{}/english/'.format(chinese_phrase))

def new_pinyin(request, chinese_phrase):
    pinyin_text = request.POST.get('pinyin', '').strip()
    if pinyin_text != '':
        phrase = add_chinese_phrase(chinese_phrase)
        update_phrase_pinyin(phrase, pinyin_text)
    return redirect('/putonghua/{}/english/'.format(chinese_phrase))

def view_english(request, chinese_phrase):
    translation = find_first_definition(chinese_phrase)
    if translation is None:
        translation = ChineseEnglishTranslation(
            simplified=chinese_phrase,
            pinyin=get_phrase_pinyin(chinese_phrase),
            english=''
            )
    definitions = list(get_definitions(chinese_phrase))
    return render(request, 'english.html',
                  {'phrase_translation'  : translation,
                   'definitions'         : definitions})

def view_hsk_list(request, list_number):
    list_number = int(list_number)
    hsk_definitions = list(hsk_word_list_translations(list_number))
    list_title = "HSK Word List {}".format(list_number)

    available_lists = []
    for i in range(1,7):
        if i == list_number: active = True
        else:                active = False
        available_lists.append({'number': i,
                                'name': "List {}".format(i),
                                'active': active})

    return render(request, 'hsk_list.html',
                  {'list_title'     : list_title,
                   'available_lists': available_lists,
                   'hsk_words'      : hsk_definitions})

def view_stats(request):
    char_cnt = Character.objects.all().count()
    phrase_cnt = ChinesePhrase.objects.all().count()
    word_cnt = ChineseWord.objects.all().count()
    name_cnt = ChineseName.objects.all().count()
                   
    site_stats = []
    site_stats.append({'title' : 
                       'Total Entries', 'value': phrase_cnt + char_cnt})
    site_stats.append({'title' : 
                       'Single Character Entries', 'value': char_cnt})
    site_stats.append({'title' : 
                       'Multi-Character Phrase Entries', 'value': phrase_cnt})
    site_stats.append({'title' : 
                       'Chinese Word Entries', 'value': word_cnt})
    site_stats.append({'title' : 
                       'Chinese Proper Names', 'value': name_cnt})
    return render(request, 'view_stats.html',
                  {'site_stats' : site_stats})

