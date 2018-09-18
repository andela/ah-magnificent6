# Generated by Django 2.1 on 2018-09-18 15:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='unread',
        ),
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.ManyToManyField(blank=True, related_name='read', to=settings.AUTH_USER_MODEL),
        ),
    ]