import os.path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from putonghua.dictionary import upload_hsk_list_file

DATA_RESOURCES = os.path.abspath(os.path.join(settings.BASE_DIR, 'putonghua/data_resources'))

class Command(BaseCommand):
    help = 'Loads all 6 HSK Word Lists from the repository'

    def handle(self, *args, **options):
        for list_num, filename in [(1, 'HSK_2012_L1_freqorder.txt'),
                                   (2, 'HSK_2012_L2_freqorder.txt'),
                                   (3, 'HSK_2012_L3_freqorder.txt'),
                                   (4, 'HSK_2012_L4_freqorder.txt'),
                                   (5, 'HSK_2012_L5_freqorder.txt'),
                                   (6, 'HSK_2012_L6_freqorder.txt')]:
            upload_hsk_list_file(os.path.join(DATA_RESOURCES, filename), list_num)

