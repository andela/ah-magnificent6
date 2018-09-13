from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

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
    favourited = models.ManyToManyField(User, related_name='favourited',
                                        blank=True)
    rating_average = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    image = models.ImageField(
        upload_to='static/images', default='static/images/no-img.jpg')
    # store the number of likes here
    likesCount = models.IntegerField(default=0)
    DislikesCount = models.IntegerField(default=0)

    def __str__(self):
        "Returns a string representation of article title."
        return self.title

    def save(self, *args, **kwargs):
        """
        Generate a slug for the article before saving it.
        """
        self.slug = slugify(self.title + '-' + uuid.uuid4().hex)
        super().save(*args, **kwargs)


class ArticleRating(models.Model):
    """
    Article schema.
    Article rating is done on a scale of 1-5 thus, the rating field will have a
    minimum value validator of 1 and a maximum value validator of 5
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])


class Likes(models.Model):
    """
    An article can be liked or disliked by users.
    This class defines fields necessary to record likes of a given article
    by users.
    """
    class Meta:
        # A user can like or dislike an article only once.
        # Making an article_id and user_id unique_together achieves
        # the intended behavior.
        unique_together = (('article', 'user'))
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # This field will be set to True if user likes an article
    # and False otherwise
    like = models.BooleanField()
