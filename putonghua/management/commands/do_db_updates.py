from django.core.management.base import BaseCommand, CommandError
from putonghua.models import CharPinyinEnglish, ChinesePhraseToEnglish
from putonghua.cedict import fix_cedict_classifier_definitions
from putonghua.cedict import change_character_classifiers_to_word_classifiers

class Command(BaseCommand):
    help = 'Handles any necessary one-time database updates (currently fixing the rank default)'

    def handle(self, *args, **options):
        for connect in CharPinyinEnglish.objects.filter(rank=0):
            connect.rank = 999
            connect.save()

        for connect in ChinesePhraseToEnglish.objects.filter(rank=0):
            connect.rank = 999
            connect.save()

        fix_cedict_classifier_definitions()
        change_character_classifiers_to_word_classifiers()
