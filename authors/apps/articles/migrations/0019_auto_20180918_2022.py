# Generated by Django 2.1 on 2018-09-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_auto_20180918_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletags',
            name='tag',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
