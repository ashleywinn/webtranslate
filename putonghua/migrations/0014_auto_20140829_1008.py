# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putonghua', '0013_auto_20140823_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseName',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('pinyin', models.TextField()),
                ('name_type', models.CharField(choices=[('P', 'Person'), ('L', 'Location/Place'), ('A', 'Artwork/Book/Movie'), ('I', 'Idea/Movement/Time period'), ('U', 'Unknown')], default='U', max_length=1)),
                ('character', models.OneToOneField(to='putonghua.Character', null=True)),
                ('phrase', models.OneToOneField(to='putonghua.ChinesePhrase', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chinesephrase',
            name='variant_of',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='englishtranslation',
            name='is_name',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
