# Generated by Django 3.1.5 on 2021-09-27 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_auto_20210926_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe_time',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='recipe',
            name='publish_day',
            field=models.DateTimeField(null=True),
        ),
    ]
