# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0007_auto_20140808_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChinesePhraseToEnglish',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('rank', models.PositiveSmallIntegerField()),
                ('englishtranslation', models.ForeignKey(to='putonghua.EnglishTranslation')),
                ('phrase', models.ForeignKey(to='putonghua.ChinesePhrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='charpinyinenglish',
            name='rank',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='definitions',
            field=models.ManyToManyField(through='putonghua.ChinesePhraseToEnglish', to='putonghua.EnglishTranslation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='phrase_md5',
            field=models.CharField(default='0', max_length=32),
            preserve_default=False,
        ),
    ]
