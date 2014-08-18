# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0006_englishtranslation_eng_md5'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chinesecharacter',
            name='translations',
        ),
        migrations.DeleteModel(
            name='ChineseCharacter',
        ),
        migrations.DeleteModel(
            name='Sentence',
        ),
    ]
