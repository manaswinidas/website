# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-12-14 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0124_auto_20181213_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialmentorfeedback',
            name='in_contact',
            field=models.BooleanField(verbose_name='Has your intern been in contact to discuss how to approach their first tasks?'),
        ),
    ]
