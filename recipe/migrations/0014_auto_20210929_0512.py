# Generated by Django 3.1.5 on 2021-09-29 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_auto_20210929_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='email',
            field=models.EmailField(error_messages={'required': 'メールアドレスを入力してください', 'unique': 'そのメールアドレスは既に使われています'}, max_length=254, unique=True, verbose_name='メールアドレス'),
        ),
    ]
