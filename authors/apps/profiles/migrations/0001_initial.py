# Generated by Django 2.1 on 2018-09-07 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, default='', null=True, verbose_name='bio')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, verbose_name='gender')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='avatar/')),
                ('city', models.CharField(default='', max_length=100, verbose_name='city')),
                ('country', models.CharField(default='', max_length=100, verbose_name='country')),
                ('phone', models.IntegerField(default=0, verbose_name='phone')),
                ('website', models.URLField(blank=True, default='', verbose_name='website')),
                ('follows', models.ManyToManyField(related_name='followed_by', to='profiles.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.timestampmodel',),
        ),
    ]
