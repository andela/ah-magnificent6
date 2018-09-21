from django.db import models
from django.contrib.contenttypes.models import ContentType

from authors.apps.authentication.models import User
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
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        "Returns a string representation of notification."
        return self.notification


def notify_follower(author, notification, article):
    """
    Function that adds a notification to the Notification model.
    in order to add them to the notified column of the notification.
    """
    created_notification = Notification.objects.create(
        notification=notification, classification="article", article=article)
    followers = author.profile.followed_by.all()

    for follower in followers:
        # checks if notification is set to True
        if follower.app_notification_enabled is True:
            created_notification.notified.add(follower.user.id)
    created_notification.save()
