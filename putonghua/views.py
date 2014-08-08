from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from putonghua.models import ChineseEnglishTranslation
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

def home_page(request):
    return render(request, 'home.html')

def new_translation(request, chinese_phrase):
    english_text = request.POST.get('english', '').strip()
    if english_text != '':
        phrase = add_chinese_phrase(chinese_phrase)
        add_english_definition(phrase, english_text)
    return redirect('/putonghua/{}/english/'.format(chinese_phrase))

def new_pinyin(request, chinese_phrase):
    pinyin_text = request.POST.get('pinyin', '').strip()
    if pinyin_text != '':
        phrase = add_chinese_phrase(chinese_phrase)
        update_phrase_pinyin(phrase, pinyin_text)
    return redirect('/putonghua/{}/english/'.format(chinese_phrase))

def new_chinese(request):
    new_phrase_text = request.POST.get('new_phrase', '').strip()
    if new_phrase_text == '':
        return redirect('/')
    return redirect('/putonghua/{}/english/'.format(new_phrase_text))

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

