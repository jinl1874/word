# Generated by Django 3.1.7 on 2021-03-26 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_user', models.CharField(max_length=128, verbose_name='修改用户')),
                ('old_password', models.CharField(max_length=256, verbose_name='旧密码')),
                ('new_password', models.CharField(max_length=256, verbose_name='新密码')),
                ('change_time', models.TimeField(auto_now_add=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '密码纪录',
                'verbose_name_plural': '密码纪录',
                'ordering': ['-change_time'],
            },
        ),
        migrations.CreateModel(
            name='UserChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_user', models.CharField(max_length=128, verbose_name='修改用户')),
                ('change_type', models.CharField(max_length=64, verbose_name='修改类型')),
                ('change_time', models.TimeField(auto_now_add=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '修改纪录',
                'verbose_name_plural': '修改纪录',
                'ordering': ['-change_time'],
            },
        ),
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('word_type', models.CharField(max_length=16, verbose_name='词库')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_nickname', models.CharField(max_length=128, verbose_name='昵称')),
                ('old_sex', models.CharField(choices=[('male', '男'), ('female', '女'), ('other', '其它')], max_length=32)),
                ('old_sign', models.CharField(max_length=256, verbose_name='签名')),
                ('old_avatar', models.ImageField(upload_to='img', verbose_name='头像')),
                ('change', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userchange')),
            ],
        ),
    ]
