# Generated by Django 2.1 on 2018-09-21 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletags',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articletags',
            name='user',
        ),
        migrations.AddField(
            model_name='article',
            name='article_tags',
            field=models.ManyToManyField(blank=True, to='articles.ArticleTags'),
        ),
        migrations.AddField(
            model_name='articlerating',
            name='article',
            field=models.ForeignKey(default=111111, on_delete=django.db.models.deletion.CASCADE, to='articles.Article'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articlerating',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article'),
        ),
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('article', 'user')},
        ),
    ]
