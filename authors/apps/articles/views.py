"""
This module defines views used in CRUD operations on articles.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.views import APIView
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication

# Add pagination
from rest_framework.pagination import PageNumberPagination

# Add search package
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from .renderers import ArticleJSONRenderer
from .serializers import (
    ArticleSerializer, ArticleRatingSerializer, LikesSerializer, TagsSerializer,
    ArticleReportSerializer, ArticleReportRetrieveSerializer
)
from .models import Article, ArticleRating, Likes, ArticleTags, ArticleReport
from authors.apps.notifications.models import notify_follower


def create_tag(tags, article):
    """
    This method checks whether a tag with tag provided exists in the database
    and creates it if it does not exist.
    :params str tag: name of the new tag or tag to query from the database
    :returns cls object ArticleTags: the tag as retrieved from the database
    """
    # retrieve all tag names and create new ones if they do not exist
    # also, add them to the articles and save the article instance

    for tag in tags.split(','):
        article_tag = ArticleTags.objects.filter(tag__icontains=tag.strip())
        if not article_tag:
            data = {'tag': tag.strip()}
            serializer = TagsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            article_tag = serializer.save()
            article.article_tags.add(article_tag)
        else:
            article.article_tags.add(article_tag.first())
    article.save()
    return None


class ArticleAPIView(generics.ListCreateAPIView):
    """
    get:
    Retrieve all articles
    post:
    Create a new article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    # Apply pagination to view
    pagination_class = PageNumberPagination
    # Add search class and fields
    filter_backends = (SearchFilter, DjangoFilterBackend, )
    # Define search and filter fields with the field names mapped to a list of lookups
    fields = {
        'author__username': ['icontains'],
        'title': ['icontains'],
        'article_tags__tag': ['icontains'],
    }

    search_fields = fields
    filter_fields = fields

    def post(self, request):
        """
        Creates an article
        :params HttpRequest: a post request with article data sent by clients
        to create a new article.
        :return aricleObject:returns a successfully created article
        """
        # Retrieve article data from the request object and convert it
        # to a kwargs object
        # get user data at this point

        article = {
            'title': request.data.get('title', None),
            'body': request.data.get('body', None),
            'description': request.data.get('description', None),
            'author': request.user.id
        }
        # pass article data to the serializer class, check whether the data is
        # valid and if valid, save it.
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        # retrieve the tags as passed on in the article data
        tags = request.data.get('tags', None)
        if tags:
            create_tag(tags, article)
        return Response(serializer.data, status.HTTP_201_CREATED)


@receiver(post_save, sender=Article)
def notify_follower_reciever(sender, instance, created, **kwargs):
    """
    Send a notification after the article being created is saved.
    """
    if created:
        message = (instance.author.username +
                   " has created an article. Title: " + instance.title)
        notify_follower(instance.author, message, instance)


class ArticleDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    put:
    delete:
    """
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None

    def get(self, request, slug):
        """
        Retrieve a specific article from the database given it's article id.
        :params str slug: a slug of an article you want to retrieve
        :returns article: a json data for the requested article
        """
        article = self.get_object(slug)
        if article:
            serializer = self.serializer_class(
                article, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            # return error message indicating article requested is not found.
            return Response({
                'error': 'Article with given id does not exist'
            }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        """
        Delete a given article.
        :params slug: a slug of the article to be deleted
                request: a request object with authenticated user credentials
        :returns json message: a json object containing message to indicate
            that the article has been deleted
        """
        article = self.get_object(slug)
        if not article:
            # return error message for non-existing article
            return Response({
                'error': 'Article with given id does not exist'
            }, status.HTTP_404_NOT_FOUND)
        # check whether user owns this article before attempting to delete it
        if article.author.id == request.user.id:
            article.delete()
            return Response(
                {
                    'message': "Article deleted successfully"
                }, status.HTTP_200_OK)
        else:
            # prevent a user from deleting an article s/he does not own
            return Response({
                'error':
                'You cannot delete articles belonging to other users.'
            }, status.HTTP_403_FORBIDDEN)

    def put(self, request, slug):
        """
        Update a single article
        :params str slug: a slug for the article to be updated
                request: a request object with new data for the article
        :returns article: An updated article in json format
        """
        article = self.get_object(slug)
        if not article:
            # Tell client we have not found the requested article
            return Response({
                'error': 'Article requested does not exist'
            }, status.HTTP_404_NOT_FOUND)
        # check whether user owns this article and proceed if they do
        if article.author.id == request.user.id:
            request.data['author'] = request.user.id
            serializer = self.serializer_class(article, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            tags = request.data.get('tags', None)
            # clear all tags in the article before adding new ones
            article.article_tags.clear()
            if tags:
                # add tags to the article
                create_tag(tags, article)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            # prevent a user from updating an article s/he does not own
            return Response(
                {
                    'error': 'You cannot edit an article you do not own.'
                }, status.HTTP_403_FORBIDDEN)


class FavoriteArticle(generics.CreateAPIView):
    """
    A user is able to favourite an article if they had not favourited it.
    If they had favourited it, the article becomes unfavourited.
    """
    permission_classes = (IsAuthenticated, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        """
        This method handles favouriting and unfavouriting of articles.
        Checks whether the article exists.
        Checks whether the user has favourited the article in order to favourite
        it or unfavourite it if the user had already favourited it.
        """
        try:
            article = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            response = {
                "message": "The article does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        user = request.user

        if user in article.favourited.all():
            # User has already favourited it, unfavourites the article
            article.favourited.remove(user.id)
            article.save()
            serializer = self.get_serializer(article)
            message = "You have successfully unfavourited this article"
            response = {"message": message, "article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            # Favourites the article
            article.favourited.add(user.id)
            article.save()
            serializer = self.get_serializer(article)
            message = "You have successfully favourited this article"
            response = {"message": message, "article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)


class ArticleRatingAPIView(generics.ListCreateAPIView):
    """
    get:
    Retrieve all article ratings
    post:
    Create a new article rating
    """
    permission_classes = (IsAuthenticated, )
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer
    renderer_classes = (ArticleJSONRenderer, )

    def post(self, request, slug):
        """
        Creates an article rating
        :params HttpRequest: A post request with article rating data sent by
        clients to create a new article rating.
        :return: Returns a successfully created article rating
        """
        # Retrieve article rating data from the request object and convert it
        # to a kwargs object
        # get user data at this point
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {'message': 'That article does not exist'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article.author.id == request.user.id:
            wink_emoji = u"\U0001F609"
            data = {
                'message':
                'We see what you did there {}. Sorry, but you cannot rate your '
                'own article.'.format(wink_emoji)
            }
            return Response(data, status.HTTP_403_FORBIDDEN)

        article_rating = {
            'article': article.id,
            'user': request.user.id,
            'rating': request.data.get('rating', None),
        }
        # pass article data to the serializer class, check whether the data is
        # valid and if valid, save it.
        serializer = self.serializer_class(data=article_rating)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Save the average article rating to the Article model
        q = ArticleRating.objects.filter(article_id=article.id).aggregate(
            Avg('rating'))
        article.rating_average = q['rating__avg']
        article.save(update_fields=['rating_average'])

        data = {"message": "Thank you for taking time to rate this article."}

        return Response(data, status.HTTP_201_CREATED)


class ArticleLikes(generics.ListCreateAPIView):
    """
    post:
    like or dislike an article
    """
    serializer_class = LikesSerializer

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None

    def post(self, request, slug):
        """
        creates an article like or a dislike
        :params HttpRequest: this request contains a user authorization token
                            and a json payload in the form{
                                "like": True/False
                            }. True is a like while False is a dislike
                slug: a slug for the article user wants to like or dislike
        :returns str:message thanking user for taking time to give their
                    opinion on this article
                status code 201: Indicates the a new record has been created
                for a lik or dislike
        """
        # Let's check whether we have the correct payload before doing any
        # database transaction since they are very expensive to us.
        # This variable, `like`, holds user intention which can be a
        # like or dislike
        like = request.data.get('like', None)
        if like is None or type(like) != type(True):
            return Response(
                {'message':
                 'You must indicate whether you like or dislike this article'
                 },
                status.HTTP_400_BAD_REQUEST)
        # we continue now since we are sure we have a valid payload
        # Check whether user has already like or dislike this article
        likes = None
        # Let's check whether the article requested exists in our
        # database and retrieve it
        article = self.get_object(slug)
        try:
            likes = Likes.objects.get(user=request.user.id, article=article)
        except ObjectDoesNotExist:
            # let's do nothing here since we are only checking whether user has
            # liked or disliked this article
            pass
        # Alert user if article does not exist
        if not article:
            return Response(
                {
                    'message': 'Article requested does not exist'
                }, status.HTTP_404_NOT_FOUND
            )
        new_like = {
            'article': article.id,
            'user': request.user.id,
            'like': like
        }
        # If there is a record for this article and the current user in the
        # system, we modify it instead of creating a new one.
        if likes:
            # user had liked the article but now wants to dislike it
            if likes.like and not like:
                article.userLikes.remove(request.user)
                article.userDisLikes.add(request.user)
            # user had disliked this article but now wants to like it
            elif not likes.like and like:
                article.userLikes.add(request.user)
                article.userDisLikes.remove(request.user)
            # elif likes.like and like
            elif like:
                # User can only like an article once or dislike an article once
                msg = '{}, you already liked this article.'.format(
                    request.user.username)
                return Response(
                    {
                        'message': msg
                    }, status.HTTP_403_FORBIDDEN
                )
            else:
                msg = '{}, you already disliked this article.'.format(
                    request.user.username)
                return Response(
                    {
                        'message': msg
                    }, status.HTTP_403_FORBIDDEN
                )
            # save the new value/state of the article
            article.save()
            # There is no need to create a new record; edit the existing one
            likes.like = like
            likes.save()
        else:
            # We don't need to do any more operations here
            # because this is user's first time to see this article
            serializer = self.serializer_class(data=new_like)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # update likes count or dislikes count for the article
            if like:
                article.userLikes.add(request.user)
            else:
                article.userDisLikes.add(request.user)
            # save the new state of our article
            article.save()
        # Tell user we are successful
        return Response(
            {
                'message': (
                    'Thank you {} for giving your opinion on this '.format(
                        request.user.username) + 'article.'
                )
            }, status.HTTP_201_CREATED
        )


class ArticleReportAPIView(generics.ListCreateAPIView):
    """
    get:
    Retrieve all article reports
    post:
    Create a new article report
    """
    permission_classes = (IsAuthenticated,)
    queryset = ArticleReport.objects.all()
    serializer_class = ArticleReportSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def list(self, request, slug):
        """Method for listing all reports."""
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                'message': 'That article does not exist.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff:
            queryset = self.get_queryset()
        else:
            queryset = ArticleReport.objects.filter(user_id=request.user.id)
        if not queryset.exists():
            response = {
                'message': 'No concerns have been raised on this article.'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleReportRetrieveSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """Method for reporting an article."""
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                'message': 'That article does not exist.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        user_report_count = ArticleReport.objects.filter(
            article_id=article.id, user_id=request.user.id).count()

        if user_report_count > 4:
            response = {
                'message':
                'You are not allowed to report an article more than five times.'
            }
            return Response(response, status=status.HTTP_200_OK)

        article_report = {
            'article': article.id,
            'user': request.user.id,
            'text': request.data.get('text', None),
        }

        # pass article data to the serializer class, check whether the data is
        # valid and if valid, save it.
        serializer = self.serializer_class(data=article_report)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Save the total number of reports flagged on this article.
        total_report_count = ArticleReport.objects.filter(
            article_id=article.id).count()
        article.report_count = total_report_count
        article.save(update_fields=['report_count'])

        data = {
            "message":
            "Your feedback has been recorded. Authors' "
            "Haven thanks you for your service."
        }

        return Response(data, status.HTTP_201_CREATED)


class ArticleReportRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Retrieve an article report
    delete:
    Delete an article report
    put:
    Update an article report
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleReportSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def get_article_object(self, pk):
        """ Getter method for an ArticleReport using pk (primary key)."""
        try:
            return ArticleReport.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get(self, request, slug, pk):
        """The method for retrievieng a sinlge Article Report."""
        article_report = self.get_article_object(pk)
        """
        Attempt to get an article using the slug.
        If article doesn't exist the user will receive a message telling them so
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                'message': 'That article does not exist.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article_report:
            if request.user.is_staff or request.user == article_report.user:
                serializer = ArticleReportRetrieveSerializer(article_report)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    'message': 'You are not allowed to view this report.'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # return error message indicating article report is not found.
            return Response(data={
                'message': 'That article report does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug, pk):
        article_report = self.get_article_object(pk)
        """
        Attempt to get an article using the slug.
        If article doesn't exist the user will receive a message telling them so
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                'message': 'That article does not exist.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article_report:
            if request.user.is_staff or request.user == article_report.user:
                article_data = {
                    'article': article_report.article.id,
                    'user': request.user.id,
                    'text': request.data.get('text', None),
                }
                serializer = self.serializer_class(
                    article_report, data=article_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    'message': 'You are not allowed to update this report.'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # return error message indicating article report is not found.
            return Response(data={
                'message': 'That article report does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug, pk):
        article_report = self.get_article_object(pk)
        """
        Attempt to get an article using the slug.
        If article doesn't exist the user will receive a message telling them so
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                'message': 'That article does not exist.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article_report:
            if request.user.is_staff or request.user == article_report.user:
                article_report.delete()

                # Save the total number of reports flagged on this article.
                total_report_count = ArticleReport.objects.filter(
                    article_id=article.id).count()
                article.report_count = total_report_count
                article.save(update_fields=['report_count'])

                return Response(data={
                    'message': "Report was deleted successfully"
                }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    'message': 'You are not allowed to delete this report.'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # return error message indicating article report is not found.
            return Response(data={
                'message': 'That article report does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
