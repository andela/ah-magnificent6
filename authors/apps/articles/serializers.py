from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (Article, ArticleRating, Likes,
                     ArticleTags, Comment, ArticleReport, Bookmark)

from ..authentication.models import User
from ..authentication.serializers import UserSerializer
from ..profiles.serializers import ProfileSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""
    favourite = serializers.SerializerMethodField(method_name='get_favorite')
    favouritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count')
    share_urls = serializers.SerializerMethodField(read_only=True)
    time_to_read = serializers.ReadOnlyField(source="get_time_to_read")
    article_tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        """Declare all fields to be returned from the model of articles."""

        model = Article
        fields = (
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
            "userLikes",
            "userDisLikes",
            "rating_average",
            "time_to_read",
            "article_tags",
            "report_count",
            "share_urls"
        )

    def get_favorite(self, instance):
        """Return True if the user has favorited an article, else False."""
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return instance.favourited.filter(pk=request.user.pk).exists()

    def get_favorites_count(self, instance):
        """Return the number of users who have favourited the atricle."""
        return instance.favourited.count()

    def get_share_urls(self, instance):
        """
        Populates the share_urls field with the urls for facebook, twitter
        and email.
        """
        request = self.context.get('request')
        return instance.get_share_uri(request=request)


class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleRating

        """
        Declare all fields we need to be returned from ArticleRating model
        """
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleRatingSerializer, self).__init__(*args, **kwargs)

        # Override the error_messages of each field with a custom error message
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['null'] = field_error_messages['blank'] \
                = field_error_messages['required'] \
                = 'Please fill in the {}'.format(field)

    def update(self, instance, validated_data):
        """
        Method for updating an existing ArticleRating object
        """
        instance.article = validated_data.get('article', instance.article)
        instance.user = validated_data.get('user', instance.user)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Method for creating an ArticleRating object
        It checks if a user has made a rating for an article. If yes it calls
        the update method. If not, it creates a new ArticleRating object.
        """
        article_rating_object, created = ArticleRating.objects.get_or_create(
            article_id=validated_data.get('article').id,
            user_id=validated_data.get('user').id,
            defaults={'rating': validated_data.get('rating', None)}, )

        if not created:
            self.update(instance=article_rating_object,
                        validated_data=validated_data)

        return article_rating_object


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Likes.objects.all(),
                fields=('article', 'user'),
                message='Sorry, you have already liked this article'
            )
        ]


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleTags
        fields = ('tag',)


class ArticleReportSerializer(serializers.ModelSerializer):
    """Serializer class for ArticleReport model."""

    class Meta:
        model = ArticleReport
        fields = '__all__'


class ArticleReportRetrieveSerializer(serializers.ModelSerializer):
    """Serializer class for Retrieving ArticleReport model."""
    user = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = ArticleReport
        fields = ('text', 'user', 'article', 'created_at', 'updated_at')

    def get_user(self, instance):
        return instance.user.username

    def get_article(self, instance):
        return instance.article.title


class CommentSerializer(serializers.ModelSerializer):
    """
    This serializer converts comments to json serializable data
    and back
    """

    class Meta:
        model = Comment
        
        fields = ['commented_by', 'created_at', 'comment_body', 'id', 'parent']


class ArticleListingField(serializers.RelatedField):
    def to_representation(self, value):
        return (value.slug)

    def to_internal_value(self, data):
        return (Article.objects.get(id=data))


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleListingField(queryset=Article.objects.all())

    class Meta:
        model = Bookmark
        """
        Declare all fields we need to be returned from ArticleRating model
        """
        fields = ('__all__')
        validators = [
            UniqueTogetherValidator(
                queryset=Bookmark.objects.all(),
                fields=('article', 'user'),
                message='Sorry, you have already bookmarked this article'
            )
        ]
