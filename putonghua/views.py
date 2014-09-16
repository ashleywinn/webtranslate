import re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from putonghua.models import Character, ChinesePhrase, ChineseWord, ChineseName
from putonghua.models import ChineseEnglishTranslation, ChineseHskWord
from putonghua.forms  import ChinesePhraseForm
from putonghua.dictionary import find_definitions
from putonghua.dictionary import add_english_definition, get_components_of_phrase
from putonghua.dictionary import get_phrase_pinyin
from putonghua.dictionary import get_toneless_pinyin_components


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
            yield from find_up_to_n_definitions(2, component)

def home_page(request):
    return render(request, 'home.html')

def search_chinese(request):
    search_text = request.POST.get('search_phrase', '').strip()
    if search_text == '':
        return redirect('/')
    if re.match(r'[a-zA-Z]', search_text) is not None:
        return redirect('pinyin_search_result', search_text)
    return redirect('view_english', search_text)

def view_english(request, chinese_phrase):
    translation = find_first_definition(str(chinese_phrase))
    if translation is None:
        translation = ChineseEnglishTranslation(
            simplified=chinese_phrase,
            pinyin=get_phrase_pinyin(chinese_phrase),
            english=''
            )
    definitions = list(get_definitions(chinese_phrase))

    form = ChinesePhraseForm(initial={'pinyin': translation.pinyin,
                                      'simplified': chinese_phrase, })
    if request.method == 'POST':
        form = ChinesePhraseForm(data=request.POST)
        if form.is_valid():
            phrase, created = ChinesePhrase.objects.get_or_create(
                simplified=chinese_phrase)
            if form.cleaned_data['english'] != '':
                add_english_definition(phrase, form.cleaned_data['english'])
            phrase.pinyin = form.cleaned_data['pinyin']
            phrase.save()
            return redirect('view_english', chinese_phrase)
            
    return render(request, 'english.html',
                  {'form'                : form,
                   'phrase_translation'  : translation,
                   'definitions'         : definitions})

def view_hsk_list(request, list_number):
    list_number = int(list_number)
    list_title = "HSK Word List {}".format(list_number)

    available_list_nums = (1, 2, 3, 4, 5, 6)
    available_lists = []
    for i in available_list_nums:
        if i == list_number: active = True
        else:                active = False
        available_lists.append({'number': i,
                                'name': "List {}".format(i),
                                'active': active})

    hsk_definitions = [hsk.compact_english_translation(definition_cnt=3)
                       for hsk in 
                       ChineseHskWord.objects.filter(hsk_list=list_number)]

    return render(request, 'hsk_list.html',
                  {'list_title'     : list_title,
                   'available_lists': available_lists,
                   'definitions'      : hsk_definitions})

def pinyin_search_result(request, pinyin):
    pinyin_components = list(get_toneless_pinyin_components(pinyin))
    definitions = []
    for component in pinyin_components:
        for phrase in ChinesePhrase.objects.filter_tonelesspinyin_exact(
                        component).order_by('-freq_score'):
            for trans in phrase.compact_english_translations(definition_cnt=3):
                definitions.append(trans)
        for character in Character.objects.filter_tonelesspinyin_exact(
                        component).order_by('-freq_score'):
            for trans in character.compact_english_translations(definition_cnt=3):
                definitions.append(trans)
    pinyin = ' '.join(pinyin_components)
    return render(request, 'pinyin_search_result.html',
                  {'search_pinyin'  : pinyin,
                   'definitions'    : definitions})

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

