# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0016_auto_20140901_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtlexworddata',
            name='simplified',
            field=models.CharField(max_length=16, default=''),
            preserve_default=False,
        ),
    ]
