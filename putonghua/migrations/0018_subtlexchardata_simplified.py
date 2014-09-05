# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0017_subtlexworddata_simplified'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtlexchardata',
            name='simplified',
            field=models.CharField(max_length=1, default=''),
            preserve_default=False,
        ),
    ]
