#!/usr/bin/env python

import os
import sys

def main():
    from putonghua.dictionary import upload_hsk_list_file
    from putonghua.models import Character

    print(sys.argv[1])
    upload_hsk_list_file(sys.argv[1], sys.argv[2])
    

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webtranslate.settings")
    import django
    django.setup()

    main()

