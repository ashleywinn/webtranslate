#!/usr/bin/env python

import os
import sys

def main():
    from putonghua.dictionary import upload_subtlex_char_data
    from putonghua.models import Character

    print(sys.argv[1])
    upload_subtlex_char_data(sys.argv[1])
    

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webtranslate.settings")
    import django
    django.setup()

    main()

