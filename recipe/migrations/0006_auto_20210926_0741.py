# Generated by Django 3.1.5 on 2021-09-26 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20210920_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='api_id',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipe.category'),
        ),
    ]
