from django.db import models
from django.utils.text import slugify
from authors.apps.authentication.models import User
import uuid


class Article(models.Model):
    """
    Defines fields for each article.
    """
    class Meta:
        # Order article by date published
        ordering = ['-published_at']

    title = models.CharField(max_length=255)
    body = models.TextField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, editable=False, max_length=140)
    favorited = models.NullBooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='static/images', default='static/images/no-img.jpg')

    def __str__(self):
        "Returns a string representation of article title."
        return self.title

    def save(self, *args, **kwargs):
        """
        Generate a slug for the article before saving it.
        """
        self.slug = slugify(self.title + '-' + uuid.uuid4().hex)
        super().save(*args, **kwargs)
