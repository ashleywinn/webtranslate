from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from putonghua.dictionary import upload_hsk_list_file

class Command(BaseCommand):
    args = '<hsk_file.txt>'
    help = 'Loads an HSK Word List into the database'
    option_list = BaseCommand.option_list + (
        make_option('--list-num', type="int", default=0,
                    help="The HSK List number [1-6]"),
        )

    def handle(self, *args, **options):
        list_number = options['list_num']
        if list_number < 1 or list_number > 6:
            raise CommandError('Requires a list number between 1 and 6')
        if len(args) != 1:
            raise CommandError('Only supports uploading 1 file at a time')
        upload_hsk_list_file(args[0], list_number)

