# Generated by Django 2.1 on 2018-09-18 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20180918_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='articletags',
            name='tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='articles.Article'),
        ),
    ]