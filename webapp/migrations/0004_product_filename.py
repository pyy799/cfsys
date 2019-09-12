# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20190910_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fileName',
            field=models.CharField(verbose_name='审核文件', blank=True, max_length=64, null=True),
        ),
    ]
