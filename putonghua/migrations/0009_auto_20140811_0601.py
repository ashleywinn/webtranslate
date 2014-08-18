# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0008_auto_20140808_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseHskWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsk_list', models.PositiveSmallIntegerField()),
                ('character', models.OneToOneField(to='putonghua.Character')),
                ('phrase', models.OneToOneField(to='putonghua.ChinesePhrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HskWordToEnglish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pinyin', models.CharField(max_length=32)),
                ('rank', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chinesehskword',
            name='definitions',
            field=models.ManyToManyField(to='putonghua.EnglishTranslation', through='putonghua.HskWordToEnglish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hskwordtoenglish',
            name='chinesehskword',
            field=models.ForeignKey(to='putonghua.ChineseHskWord'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hskwordtoenglish',
            name='englishtranslation',
            field=models.ForeignKey(to='putonghua.EnglishTranslation'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SubtlexCharData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('character', models.OneToOneField(to='putonghua.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubtlexWordData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('phrase', models.OneToOneField(to='putonghua.ChinesePhrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='character',
            name='freq_score',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='freq_score',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='chinesephrase',
            name='translations',
        ),
    ]
