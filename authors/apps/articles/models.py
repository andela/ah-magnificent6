from django.db import models
from django.utils.text import slugify
from authors.apps.authentication.models import User


class Article(models.Model):
    """
    Defines fields for each article.
    """
    class Meta:
        ordering = ['-published_at']

    title = models.CharField(max_length=255)
    body = models.TextField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, editable=False, max_length=140)
    favorited = models.BooleanField(default=False, null=True)
    favoritesCount = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='static/images', default='pic_folder/None/no-img.jpg')

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        slug = slugify(self.title)
        num = 1
        while Article.objects.filter(slug=slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
