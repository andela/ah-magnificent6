import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, max_length=140, unique=True)),
                ('rating_average', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('image', models.ImageField(default='static/images/no-img.jpg', upload_to='static/images')),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='ArticleRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article')),
            ],
        ),
    ]