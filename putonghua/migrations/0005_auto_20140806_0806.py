# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0004_auto_20140722_0238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('char', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('char_type', models.CharField(choices=[('S', 'Simplified'), ('T', 'Traditional')], max_length=1)),
                ('pinyin', models.CharField(max_length=16)),
                ('classifiers', models.CharField(blank=True, max_length=8)),
                ('alternate_char', models.CharField(blank=True, max_length=1)),
                ('variant_of', models.CharField(blank=True, max_length=1)),
                ('composed_of', models.CharField(blank=True, max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharPinyinEnglish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pinyin', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='character',
            name='translations',
            field=models.ManyToManyField(to='putonghua.EnglishTranslation', through='putonghua.CharPinyinEnglish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charpinyinenglish',
            name='character',
            field=models.ForeignKey(to='putonghua.Character'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charpinyinenglish',
            name='englishtranslation',
            field=models.ForeignKey(to='putonghua.EnglishTranslation'),
            preserve_default=True,
        ),
    ]
