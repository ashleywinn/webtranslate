# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0010_auto_20140811_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseWord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('classifiers', models.CharField(max_length=8, blank=True)),
                ('character', models.OneToOneField(null=True, to='putonghua.Character')),
                ('phrase', models.OneToOneField(null=True, to='putonghua.ChinesePhrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
