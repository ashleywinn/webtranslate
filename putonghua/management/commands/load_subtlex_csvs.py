import os.path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from putonghua.subtlex import upload_subtlex_char_data, update_char_freq_scores
from putonghua.subtlex import upload_subtlex_word_data, update_word_freq_scores

DATA_RESOURCES = os.path.abspath(os.path.join(settings.BASE_DIR, 'putonghua/data_resources'))

class Command(BaseCommand):
    help = "Loads both the 'word' and 'char' Subtlex data sets from the repository"

    def handle(self, *args, **options):
        upload_subtlex_char_data(os.path.join(DATA_RESOURCES, 'SUBTLEX-CH-CHR.csv'))
        upload_subtlex_word_data(os.path.join(DATA_RESOURCES, 'SUBTLEX-CH-WF.csv'))
        update_char_freq_scores()
        update_word_freq_scores()

