from rest_framework import serializers

from .models import Notification

from authors.apps.articles.serializers import ArticleSerializer
from django.utils.timesince import timesince


class NotificationSerializer(serializers.ModelSerializer):
    article = ArticleSerializer('article')
    timestance = serializers.SerializerMethodField(method_name='timesince')
    unread = serializers.SerializerMethodField(method_name='read')

    class Meta:
        """
        Notification fields to be returned to users
        """
        model = Notification
        fields = ('unread', 'created_at', 'notification', 'classification',
                  'article', 'timestance')

    def timesince(self, instance, now=None):
        """
        Get the time difference of the notification with the current time.
        """
        return timesince(instance.created_at, now)

    def read(self, instance):
        """
        bjnklm
        """
        request = self.context.get('request')
        if request.user in instance.read.all():
            return False
        else:
            return True
