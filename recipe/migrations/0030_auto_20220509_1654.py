# Generated by Django 3.1.5 on 2022-05-09 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0029_auto_20220509_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='api_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
