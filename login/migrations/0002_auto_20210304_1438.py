# Generated by Django 3.1.7 on 2021-03-04 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confirmstring',
            options={'ordering': ['-c_time'], 'verbose_name': '确认码', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-c_time'], 'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterModelOptions(
            name='userdetail',
            options={'ordering': ['-last_edit'], 'verbose_name': '用户信息', 'verbose_name_plural': '用户'},
        ),
    ]
