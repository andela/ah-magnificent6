from django.db import models
from django.contrib.contenttypes.models import ContentType

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article


class Notification(models.Model):
    """
    Defines fields for notifications.
    """

    class Meta:
        # Order ntification by time notified
        ordering = ['-created_at']

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.ManyToManyField(
        User, related_name='notified', blank=True)
    read = models.ManyToManyField(User, related_name='read', blank=True)
    classification = models.TextField(default="article")

    def __str__(self):
        "Returns a string representation of notification."
        return self.notification


def notify_follower(author, notification, article):
    n = Notification.objects.create(
        notification=notification, classification="article", article=article)
    profile = author.profile
    followers = profile.followed_by.all()

    for follower in followers:
        if follower.notification is True:
            n.notified.add(follower.user.id)
    n.save()


def notify_favourite(article, notification):
    n = Notification.objects.create(
        notification=notification, classification="comment")

    for user in article.favourited.all():
        if user.profile.notification is True:
            n.notified.add(user.id)
    n.save()
