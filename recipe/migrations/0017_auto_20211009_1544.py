# Generated by Django 3.1.5 on 2021-10-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0016_auto_20210929_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayIngredientOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='api_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
