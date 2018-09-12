from rest_framework import serializers
from .models import Article
from ..authentication.models import User
from ..authentication.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""

    class Meta:
        """Declare all fields to be returned from the model of articles."""

        model = Article
        fields = '__all__'
