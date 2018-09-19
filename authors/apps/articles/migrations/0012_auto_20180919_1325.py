# Generated by Django 2.1 on 2018-09-19 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20180918_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_body',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='time_stamp',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Comment'),
        ),
    ]
