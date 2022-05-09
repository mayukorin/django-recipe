# Generated by Django 3.1.5 on 2022-05-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0030_auto_20220509_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='api_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='english_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='hiragana_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='api_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]