# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-21 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_created_at'),
        ('dashboard', '0002_auto_20180121_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_maker',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comments_made', to='users.User'),
            preserve_default=False,
        ),
    ]
