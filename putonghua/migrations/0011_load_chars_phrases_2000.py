# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def load_2000_chars_and_phrases(apps, schema_editor):
    call_command("loaddata", "chars_phrases_2000.json")    

class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0010_auto_20140811_0610'),
    ]

    operations = [
        migrations.RunPython(load_2000_chars_and_phrases),
    ]
