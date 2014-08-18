#!/usr/bin/env python

import os
import sys

def main():
    from putonghua.dictionary import serialize_most_common_characters_and_phrases

    serialize_most_common_characters_and_phrases(int(sys.argv[2]), int(sys.argv[3]), sys.argv[1])
    

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webtranslate.settings")
    import django
    django.setup()

    main()

