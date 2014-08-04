# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0003_auto_20140710_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseCharacter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('simplified', models.CharField(max_length=1)),
                ('traditional', models.CharField(max_length=1)),
                ('pinyin', models.CharField(max_length=16)),
                ('translations', models.ManyToManyField(to='putonghua.EnglishTranslation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='TraditionalToSimplified',
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='length',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='englishtranslation',
            name='english',
            field=models.TextField(),
        ),
    ]
