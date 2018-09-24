# Generated by Django 2.1 on 2018-09-22 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20180921_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='articles.Article'),
        ),
    ]