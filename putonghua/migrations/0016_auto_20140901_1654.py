# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0015_auto_20140830_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishtranslation',
            name='eng_md5',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
