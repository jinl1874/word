# Generated by Django 3.1.7 on 2021-04-06 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210406_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchange',
            name='change_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='修改时间'),
        ),
    ]