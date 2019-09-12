# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_product_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uploader',
            field=models.ForeignKey(null=True, related_name='uploader', blank=True, to='webapp.UserProfile', verbose_name='上传者'),
        ),
    ]
