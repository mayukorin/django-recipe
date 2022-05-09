# Generated by Django 3.1.5 on 2022-05-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0026_auto_20220509_1653'),
    ]

    operations = [
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
    ]