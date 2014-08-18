# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0009_auto_20140811_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chinesehskword',
            name='character',
            field=models.OneToOneField(to='putonghua.Character', null=True),
        ),
        migrations.AlterField(
            model_name='chinesehskword',
            name='phrase',
            field=models.OneToOneField(to='putonghua.ChinesePhrase', null=True),
        ),
    ]
