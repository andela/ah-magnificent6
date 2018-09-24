import uuid
import re

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.reverse import reverse as api_reverse

from authors.apps.authentication.models import User
from authors import settings


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
    favourited = models.ManyToManyField(
        User, related_name='favourited', blank=True)
    rating_average = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    report_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='static/images', default='static/images/no-img.jpg')
    # store users who have liked/disliked this article here
    userLikes = models.ManyToManyField(
        User, blank=True, related_name='Likes.user+')
    userDisLikes = models.ManyToManyField(
        User, blank=True, related_name='Likes.user+')
    article_tags = models.ManyToManyField(
        'ArticleTags', blank=True)

    def __str__(self):
        "Returns a string representation of article title."
        return self.title

    def save(self, *args, **kwargs):
        """
        Generate a slug for the article before saving it.
        """
        if not self.slug:
            self.slug = slugify(self.title + '-' +
                                uuid.uuid4().hex[:6])
        super().save(*args, **kwargs)

    def get_share_uri(self, request=None):
        """
        Method to prepare and generate urls  for sharing the article to facebook,
        twitter and email.
        """
        absolute_share_uri = api_reverse(
            'articles:retrieveUpdateDelete',
            kwargs={'slug': self.slug},
            request=request)

        uri_data = {
            'twitter':
                'https://twitter.com/intent/tweet?url={}'.format(
                    absolute_share_uri),
            'facebook':
                'https://www.facebook.com/sharer/sharer.php?u={}'.format(
                    absolute_share_uri),
            'email':
                'mailto:?subject=New Article Alert&body={}'.format(
                    absolute_share_uri)
        }

        return uri_data

    @property
    def get_time_to_read(self):
        # Set the standard read time
        words_per_min = settings.WORDS_PER_MIN
        """
        Cleaning the post content and lower casing all words:
        """
        # Removing characters from the post and replacing with space for easier conversion to a list
        post = re.sub(r'[^\w]', ' ', self.body)
        # Using split to return a list of words from the post: split() returns a list of words delimited by sequences of whitespace e.g ['Cleaning', 'the', 'post', 'content' ]
        words_list = post.split()
        # Grabbing the length of the list returned by `split()` and converting toan `int` for division
        words_in_article = int(len(words_list))
        # Using double-slash to round down to nearest whole number
        read_time = words_in_article // int(words_per_min)
        # Return 1 min when the read time is less than 1
        if read_time < 1:
            return '1 min'
        return str(read_time) + ' min'


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


class ArticleTags(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag


class ArticleReport(models.Model):
    """
    Article Report schema.
    Article can be reported when they violate the terms and conditions of Authors'
    Haven.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """
    This class defines fields necessary to record comments
    on an article
    """

    commented_by = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.commented_by.username


class Bookmark(models.Model):
    """
    An article can be bookmarked by users for future reading.
    This class defines fields necessary to bookmark an article.
    """
    class Meta:
        # A user can bookmark an article only once.
        # Making an article_id and user_id unique_together achieves
        # the intended behavior.
        unique_together = (('article', 'user'))
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.slug
