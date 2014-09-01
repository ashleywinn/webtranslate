# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0014_auto_20140829_1008'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charpinyinenglish',
            options={'ordering': ['rank']},
        ),
        migrations.AlterModelOptions(
            name='chinesephrasetoenglish',
            options={'ordering': ['rank']},
        ),
        migrations.AlterField(
            model_name='charpinyinenglish',
            name='rank',
            field=models.PositiveSmallIntegerField(default=999),
        ),
        migrations.AlterField(
            model_name='chinesephrasetoenglish',
            name='rank',
            field=models.PositiveSmallIntegerField(default=999),
        ),
    ]
