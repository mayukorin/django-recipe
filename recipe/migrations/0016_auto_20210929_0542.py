# Generated by Django 3.1.5 on 2021-09-29 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0015_auto_20210929_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='username',
            field=models.CharField(max_length=150, verbose_name='ユーザ名'),
        ),
    ]
