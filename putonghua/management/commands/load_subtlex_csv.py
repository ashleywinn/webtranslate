from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from putonghua.subtlex import upload_subtlex_char_data, update_char_freq_scores
from putonghua.subtlex import upload_subtlex_word_data, update_word_freq_scores


class Command(BaseCommand):
    args = '<subtlex_data.csv>'
    help = 'Used to Load Subtlex freq data into the database'
    option_list = BaseCommand.option_list + (
        make_option('--data-type', type="choice",
                    choices=('word', 'char'),
                    help="'word' or 'char' data"),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Only supports uploading 1 file at a time')
        if options['data_type'] == 'char':
            upload_subtlex_char_data(args[0])
            update_char_freq_scores()
        else:
            upload_subtlex_word_data(args[0])
            update_word_freq_scores()

