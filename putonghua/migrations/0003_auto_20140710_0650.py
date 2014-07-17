# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0002_sentence_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChinesePhrase',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('simplified', models.TextField()),
                ('pinyin', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnglishTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('english', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='translations',
            field=models.ManyToManyField(to='putonghua.EnglishTranslation'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TraditionalToSimplified',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('traditional', models.TextField()),
                ('simplified', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
