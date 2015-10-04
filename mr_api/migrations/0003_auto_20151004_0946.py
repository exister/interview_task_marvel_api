# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mr_api', '0002_auto_20151004_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='user',
            field=models.ForeignKey(related_name='auth_token', to=settings.AUTH_USER_MODEL),
        ),
    ]
