

# Generated by Django 2.1 on 2018-09-20 13:00

# Generated by Django 2.1 on 2018-09-18 13:24



from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='last name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='last name')),
                ('bio', models.TextField(blank=True, default='', null=True, verbose_name='bio')),
                ('avatar', models.URLField(blank=True, null=True, verbose_name='avatar')),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='city')),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='country')),
                ('phone', models.IntegerField(blank=True, default=0, null=True, verbose_name='phone')),
                ('website', models.URLField(blank=True, default='', null=True, verbose_name='website')),

                ('app_notification_enabled', models.BooleanField(default=True)),

                ('follows', models.ManyToManyField(related_name='followed_by', to='profiles.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.timestampmodel',),
        ),
    ]
