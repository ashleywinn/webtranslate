# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0012_chinesehskword_chineseword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hskwordtoenglish',
            name='chinesehskword',
        ),
        migrations.RemoveField(
            model_name='hskwordtoenglish',
            name='englishtranslation',
        ),
        migrations.RemoveField(
            model_name='chinesehskword',
            name='character',
        ),
        migrations.RemoveField(
            model_name='chinesehskword',
            name='definitions',
        ),
        migrations.DeleteModel(
            name='HskWordToEnglish',
        ),
        migrations.RemoveField(
            model_name='chinesehskword',
            name='phrase',
        ),
    ]
