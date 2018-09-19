from rest_framework import serializers

from .models import Notification

from authors.apps.articles.serializers import ArticleSerializer
from django.utils.timesince import timesince


class NotificationSerializer(serializers.ModelSerializer):
    article = ArticleSerializer('article')
    timestance = serializers.SerializerMethodField(
        method_name='calculate_timesince')
    unread = serializers.SerializerMethodField(method_name='read')

    class Meta:
        """
        Notification fields to be returned to users
        """
        model = Notification
        fields = ('unread', 'created_at', 'notification', 'classification',
                  'article', 'timestance')

    def calculate_timesince(self, instance, now=None):
        """
        Get the time difference of the notification with the current time.
        """
        return timesince(instance.created_at, now)

    def read(self, instance):
        """
        Check if user has read the article.
        Returns True or False to the serializer.
        """
        request = self.context.get('request')
        if request.user in instance.read.all():
            return False
        else:
            return True
