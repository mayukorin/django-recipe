# Generated by Django 3.1.5 on 2022-05-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0023_auto_20220509_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='english_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='hiragana_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]