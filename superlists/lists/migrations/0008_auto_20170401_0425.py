# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-01 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20170330_0438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default='', unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('list', 'text')]),
        ),
    ]
