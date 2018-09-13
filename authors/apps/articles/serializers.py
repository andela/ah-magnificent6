from rest_framework import serializers
from .models import Article
from ..authentication.models import User
from ..authentication.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""
    favourite = serializers.SerializerMethodField(method_name='get_favorite')
    favouritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count')

    class Meta:
        """Declare all fields to be returned from the model of articles."""

        model = Article
        fields = (
            "id",
            "title",
            "body",
            "description",
            "created_at",
            "updated_at",
            "published_at",
            "slug",
            "image",
            "author",
            "favourited",
            "favourite",
            "favouritesCount",
        )

    def get_favorite(self, instance):
        """Return True if the user has favorited an article, else False."""
        request = self.context.get('request', None)
        if request is None:
            return False
        if not request.user.is_authenticated:
            return False
        return instance.favourited.filter(pk=request.user.pk).exists()

    def get_favorites_count(self, instance):
        """Return the number of users who have favourited the atricle."""
        return instance.favourited.count()
