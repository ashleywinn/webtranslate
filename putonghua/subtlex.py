import math
from django.db.models import Sum
from putonghua.models import SubtlexCharData, SubtlexWordData
from putonghua.models import ChinesePhrase, Character
from putonghua.models import ChineseWord
from putonghua.CsvUtil import csv_dict_iter

class SubtlexError(Exception): pass

def calc_frequency_score(cnt, tot_cnt, scale=50000):
    return int(100 * math.log1p(float(cnt) / (float(tot_cnt) / float(scale))))


def upload_subtlex_char_data(infile):
    for record in csv_dict_iter(infile, headings_row=2):
        char = record['Character'].strip()
        if len(char) == 0: continue
        if len(char) > 1:
            raise SubtlexError("found multi-character string: " + char)
        count = int(record['CHRCount'])
        try:
            if count != SubtlexCharData.objects.get(simplified=char).count:
                raise SubtlexError(
                    "new subtlex count: {} differs from saved value {}".format(count,
                      SubtlexCharData.objects.get(simplified=char).count))
            continue
        except SubtlexCharData.DoesNotExist:
            SubtlexCharData.objects.create(simplified=char, count=count)

def upload_subtlex_word_data(infile):
    for record in csv_dict_iter(infile, headings_row=2):
        word = record['Word'].strip()
        count = int(record['WCount'])
        try:
            if count != SubtlexWordData.objects.get(simplified=word).count:
                raise SubtlexError(
                   "for {} new subtlex count: {} differs from saved value {}".format(
                       word, count, SubtlexCharData.objects.get(simplified=char).count))
            continue
        except SubtlexWordData.DoesNotExist:
            SubtlexWordData.objects.create(simplified=word, count=count)

def update_char_freq_scores():
    data_set_size = SubtlexCharData.objects.all().aggregate(total=Sum('count'))['total']
    for subtlex_char in SubtlexCharData.objects.all():
        try:
            character = Character.objects.get(char=subtlex_char.simplified)
            character.freq_score = calc_frequency_score(subtlex_char.count, data_set_size)
            character.save()
        except Character.DoesNotExist:
            pass
            # print("Unrecognized char in Subtlex data: " + subtlex_char.simplified)

def update_word_freq_scores():
    data_set_size = SubtlexWordData.objects.all().aggregate(total=Sum('count'))['total']
    for subtlex_word in SubtlexWordData.objects.all():
        try:
            word = ChineseWord.objects.get_simplified_exact(subtlex_word.simplified)
            word.freq_score = calc_frequency_score(subtlex_word.count, data_set_size)
            word.save()
            try:
                word.phrase.freq_score = word.freq_score
                word.phrase.save()
            except AttributeError:
                pass
            continue
        except ChineseWord.DoesNotExist: pass
        
        try:
            phrase = ChinesePhrase.objects.get(simplified=subtlex_word.simplified)
            phrase.freq_score = calc_frequency_score(subtlex_word.count, data_set_size)
            phrase.save()
            ChineseWord.objects.create(phrase=phrase,
                                       freq_score=phrase.freq_score)
            continue
        except ChinesePhrase.DoesNotExist: 
            pass

        try:
            character = Character.objects.get(char=subtlex_word.simplified)
            ChineseWord.objects.create(character=character,
                                       freq_score=calc_frequency_score(subtlex_word.count, data_set_size))
            continue
        except Character.DoesNotExist: 
            pass
        # if neither the character or phrase exists, we won't create them now
            




    
    
