# Generated by Django 3.1.4 on 2021-04-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_id', models.IntegerField(verbose_name='noteID')),
                ('username', models.CharField(max_length=64)),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='noteID')),
                ('username', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('t_time', models.DateTimeField(auto_now=True, verbose_name='transform_time')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
                'ordering': ['-c_time'],
            },
        ),
    ]
