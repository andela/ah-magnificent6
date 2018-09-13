from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
<<<<<<< HEAD


from .models import Article, ArticleRating
=======
from .models import Article, Likes
>>>>>>> [feat]: like or dislike an article
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
<<<<<<< HEAD


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
            defaults={'rating': validated_data.get('rating', None)},)

        if not created:
            self.update(instance=article_rating_object,
                        validated_data=validated_data)

        return article_rating_object
=======
        """
        Declare all fields we need to be returned from the model of articles
        """
        fields = '__all__'


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
>>>>>>> [feat]: like or dislike an article
