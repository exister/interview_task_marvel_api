# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    User = get_user_model()
    try:
        User.objects.create_user(username='test', password='test')
    except Exception as e:
        print e


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('mr_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
