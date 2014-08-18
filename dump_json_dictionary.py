#!/usr/bin/env python

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webtranslate.settings")

from putonghua.dictionary import serialize_character_dictionary
from putonghua.models import Character


def main():
    print(sys.argv[1])
    print(Character.objects.all()[200].char)

    serialize_character_dictionary(sys.argv[1])
    

if __name__ == '__main__':
    main()

