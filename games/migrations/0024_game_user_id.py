# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 08:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0023_auto_20170920_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
