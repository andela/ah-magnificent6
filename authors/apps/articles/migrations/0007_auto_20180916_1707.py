# Generated by Django 2.1 on 2018-09-16 14:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0006_auto_20180916_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='DislikesCount',
        ),
        migrations.RemoveField(
            model_name='article',
            name='likesCount',
        ),
        migrations.AddField(
            model_name='article',
            name='userDisLikes',
            field=models.ManyToManyField(blank=True, related_name='_article_userDisLikes_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='userLikes',
            field=models.ManyToManyField(blank=True, related_name='_article_userLikes_+', to=settings.AUTH_USER_MODEL),
        ),
    ]