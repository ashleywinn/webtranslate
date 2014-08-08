# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0005_auto_20140806_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='englishtranslation',
            name='eng_md5',
            field=models.CharField(max_length=32, default='0'),
            preserve_default=False,
        ),
    ]
