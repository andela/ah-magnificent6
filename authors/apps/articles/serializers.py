from rest_framework import serializers
from .models import Article
from ..authentication.models import User
from ..authentication.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    # The statement below helps nest user details in data for an article.
    # author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        """
        Declare all fields we need to be returned from the model of articles
        """
        fields = '__all__'
        # depth = 1
