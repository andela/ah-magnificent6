from django.db import models
from django.utils.text import slugify
from authors.apps.authentication.models import User


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

    def _generate_unique_slug(self):
        """
        Generates a unique slug for the new article.
        :Returns str:slug-a unique string for each article
        """
        slug = slugify(self.title)
        new_slug = slug
        num = 1
        while Article.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(slug, num)
            num += 1
        return new_slug

    def save(self, *args, **kwargs):
        """
        Checks whether slug has been set and if not calls a method to generate
        a unique new one before saving a new article
        """
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
