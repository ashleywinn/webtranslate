# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0011_chineseword'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinesehskword',
            name='chineseword',
            field=models.OneToOneField(to='putonghua.ChineseWord', null=True),
            preserve_default=True,
        ),
    ]
