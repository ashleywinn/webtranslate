from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from putonghua.models import Sentence

def search_dict_for_string(chin_str):
    # chin_str = chin_str.strip()
    with open('putonghua/cedict_1_0_ts_utf-8_mdbg.txt') as f:
        for line in f:
            if line.startswith('#'): continue
            trad, simp, rest = line.split(None, 2)
            if trad == chin_str:
                return line
            if simp == chin_str:
                return line
        return ''

def iterate_through_string(text):
    max_chars = 6
    for i in range(len(text)):
        last_idx = i + max_chars
        if last_idx > len(text):
            last_idx = len(text)
        for j in range(last_idx, i, -1):
            yield text[i:j]

def get_defintions_list(chin_str):
    if not chin_str:
        return []
    definitions = []
    for sub_phrase in iterate_through_string(chin_str):
        definition = search_dict_for_string(sub_phrase)
        if definition != '':
            definitions.append(definition)
    return definitions


def home_page(request):
    if request.method == 'POST':
        new_sentence_text = request.POST.get('new_phrase', '').strip()
        if new_sentence_text:
            Sentence.objects.create(text=new_sentence_text)
        return redirect('/')
    
    definitions = []
    try:
        definitions = get_defintions_list(Sentence.objects.last().text)
    except AttributeError:
        pass
    
    return render(request, 'home.html',
                  {'definitions': definitions})
