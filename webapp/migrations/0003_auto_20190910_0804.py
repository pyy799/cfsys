# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20190910_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ACT', models.CharField(max_length=32, choices=[(1, '属性'), (2, '属性大类'), (3, '属性小类')], verbose_name='类型')),
                ('attribute', models.CharField(max_length=32, verbose_name='属性缩写')),
                ('first_class', models.CharField(max_length=32, null=True, verbose_name='大类缩写', blank=True)),
                ('second_class', models.CharField(max_length=32, null=True, verbose_name='小类缩写', blank=True)),
                ('meaning', models.CharField(max_length=32, null=True, verbose_name='含义', blank=True)),
                ('information', models.CharField(max_length=1024, null=True, verbose_name='备注', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('productNum', models.CharField(max_length=32, verbose_name='产品编号')),
                ('productName', models.CharField(max_length=64, verbose_name='产品名称')),
                ('pCompany', models.IntegerField(choices=[(1, '股份'), (2, '精一'), (3, '科威'), (4, '医疗'), (5, ' 柏克'), (6, '科技'), (7, '浙子')], null=True, verbose_name='公司', blank=True)),
                ('department', models.CharField(max_length=32, null=True, verbose_name='部门', blank=True)),
                ('upload_time', models.DateField(null=True, blank=True, verbose_name='审核通过日期')),
                ('introduction', models.CharField(max_length=1024, null=True, verbose_name='产品介绍', blank=True)),
                ('attribute_num', models.CharField(max_length=32, null=True, verbose_name='属性编号', blank=True)),
                ('status', models.IntegerField(choices=[(1, '待提交'), (2, '待审核'), (3, '审核通过'), (4, '审核不通过')], verbose_name='产品状态', default=1)),
                ('reason', models.CharField(max_length=1024, null=True, verbose_name='不通过原因', blank=True)),
                ('business', models.ForeignKey(blank=True, null=True, related_name='business', verbose_name='业务领域', to='webapp.Attribute')),
                ('independence', models.ForeignKey(blank=True, null=True, related_name='independence', verbose_name='自主程度', to='webapp.Attribute')),
                ('maturity', models.ForeignKey(blank=True, null=True, related_name='maturity', verbose_name='成熟度', to='webapp.Attribute')),
                ('technology', models.ForeignKey(blank=True, null=True, related_name='technology', verbose_name='技术形态', to='webapp.Attribute')),
            ],
        ),
        migrations.RenameField(
            model_name='role',
            old_name='role_name',
            new_name='roleName',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.CharField(max_length=32, null=True, verbose_name='部门', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='isValid',
            field=models.BooleanField(verbose_name='是否有效', default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='uCompany',
            field=models.IntegerField(choices=[(1, '股份'), (2, '精一'), (3, '科威'), (4, '医疗'), (5, ' 柏克'), (6, '科技'), (7, '浙子')], null=True, verbose_name='公司', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='userName',
            field=models.CharField(max_length=32, verbose_name='中文名', default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='userPassword',
            field=models.CharField(max_length=32, verbose_name='密码', default='123456'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='userRole',
            field=models.ForeignKey(related_name='user_role', blank=True, default=1, verbose_name='用户角色', to='webapp.Role'),
        ),
        migrations.AddField(
            model_name='product',
            name='uploader',
            field=models.ForeignKey(to='webapp.UserProfile', verbose_name='上传者', related_name='uploader'),
        ),
    ]
