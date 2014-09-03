import os.path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from putonghua.cedict import upload_cedict_file

DATA_RESOURCES = os.path.abspath(os.path.join(settings.BASE_DIR, 'putonghua/data_resources'))

class Command(BaseCommand):
    help = 'Load the massive cedict file from the repository'

    def handle(self, *args, **options):
        if len(args) == 0:
            upload_cedict_file(os.path.join(DATA_RESOURCES, 'cedict_1_0_ts_utf-8_mdbg.txt'))

        for arg in args:
            upload_cedict_file(arg)
            

