# Generated by Django 3.1.5 on 2021-09-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20210927_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='publish_day',
            field=models.CharField(default='', max_length=100),
        ),
    ]
