# Generated by Django 2.1 on 2018-09-13 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20180913_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='favourited',
            new_name='favorited',
        ),
    ]
