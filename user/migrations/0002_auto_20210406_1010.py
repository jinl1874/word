# Generated by Django 3.1.7 on 2021-04-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dynamics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='username')),
                ('doing', models.CharField(max_length=512, verbose_name='doing')),
                ('target_id', models.IntegerField(verbose_name='target_id')),
                ('type', models.CharField(max_length=2, verbose_name='type')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='time')),
            ],
        ),
        migrations.AlterField(
            model_name='userword',
            name='username',
            field=models.CharField(max_length=128, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='userword',
            name='word_type',
            field=models.CharField(max_length=16, verbose_name='word_type'),
        ),
    ]
