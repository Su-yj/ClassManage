# Generated by Django 2.1.4 on 2018-12-29 04:35

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='老师姓名')),
                ('gender', models.BooleanField(default=False, verbose_name='性别')),
                ('account', models.CharField(default=teacher.models.random_account, max_length=50, verbose_name='账号')),
                ('password', models.CharField(default='fd3d69aafa0d649b44d7d6cdf4c6159937cadac5', max_length=40, verbose_name='密码')),
            ],
            options={
                'verbose_name': '老师信息',
                'verbose_name_plural': '老师信息',
            },
        ),
    ]