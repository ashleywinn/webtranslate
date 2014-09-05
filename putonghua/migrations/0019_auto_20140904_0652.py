# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0018_subtlexchardata_simplified'),
    ]

    operations = [
        migrations.AddField(
            model_name='chineseword',
            name='freq_score',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='subtlexchardata',
            name='character',
        ),
        migrations.RemoveField(
            model_name='subtlexworddata',
            name='phrase',
        ),
    ]
