# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, serialize=False, to='auth.Group', auto_created=True, primary_key=True)),
                ('role_name', models.CharField(max_length=32, verbose_name='角色名称')),
                ('pSearch', models.BooleanField(verbose_name='产品信息查询权限', default=False)),
                ('pInfoNew', models.BooleanField(verbose_name='产品信息管理_新建', default=False)),
                ('pInfoUpdate', models.BooleanField(verbose_name='产品信息管理_更新', default=False)),
                ('pInfoCheck', models.BooleanField(verbose_name='产品信息管理_审核', default=False)),
                ('pAttritube', models.BooleanField(verbose_name='产品属性管理', default=False)),
                ('userManagement', models.BooleanField(verbose_name='用户权限管理_用户', default=False)),
                ('roleManagement', models.BooleanField(verbose_name='用户权限管理_角色', default=False)),
            ],
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, serialize=False, to=settings.AUTH_USER_MODEL, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30, verbose_name='中文名')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
