# Generated by Django 3.1.5 on 2021-09-29 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_auto_20210929_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='username',
            field=models.CharField(blank=True, error_messages={'blank': 'ユーザ名を入力してください', 'max_length': '名前は150字以内で入力してください', 'required': 'ユーザ名を入力してください'}, max_length=150, verbose_name='ユーザ名'),
        ),
    ]