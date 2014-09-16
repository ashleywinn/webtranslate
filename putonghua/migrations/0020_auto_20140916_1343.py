# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0019_auto_20140904_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishtranslation',
            name='eng_md5',
            field=models.CharField(unique=True, blank=True, max_length=32),
        ),
    ]
