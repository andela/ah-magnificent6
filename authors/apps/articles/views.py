"""
This module defines views used in CRUD operations on articles.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from .serializers import ArticleSerializer
from django.views.generic import ListView
from rest_framework.views import APIView
from .models import Article
from .renderers import ArticleJSONRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication


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

    def post(self, request):
        """
        Creates an article
        :params HttpRequest: a post request with article data sent by clients
        to create a new article.
        :return:returns a successfully created article
        """
        permission_classes = (IsAuthenticated, )
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
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ArticleDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    put:
    delete:
    """
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer, )

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific article from the database given it's article id.
        :params pk: an id of the article to retrieve
        :returns article: a json data for requested article
        """
        article = self.get_object(pk)
        if article:
            serializer = self.serializer_class(article)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            # return error message indicating article requested is not found.
            return Response({
                'error': 'Article with given id does not exist'
            }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete a given article.
        :params pk: an id of the article to be deleted
                request: a request object with authenticated user credentials
        :returns dict: a json object containing message to indicate that the
        article has been deleted
        """
        permission_classes = (IsAuthenticated, )
        article = self.get_object(pk)
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
                    'message': "Article with id={} deleted".format(int(pk))
                }, status.HTTP_200_OK)
        else:
            # prevent a user from deleting an article s/he does not own
            return Response({
                'error':
                'You cannot delete articles belonging\
                to other users.'
            }, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """
        Update a single article
        :params pk: an id for the article to be updated
                request: a request object with new data for the article
        """
        permission_classes = (IsAuthenticated, )
        article = self.get_object(pk)
        if not article:
            # Tell client we have not found the requested article
            return Response({
                'error': 'Article with given id does not exist'
            }, status.HTTP_404_NOT_FOUND)
        # check whether user owns this article and proceed if they do
        if article.author.id == request.user.id:
            request.data['author'] = request.user.id
            serializer = self.serializer_class(article, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            # prevent a user from updating an article s/he does not own
            return Response(
                {
                    'error': 'You cannot edit an article you do not own. '
                }, status.HTTP_403_FORBIDDEN)


class FavoriteArticle(generics.ListCreateAPIView):
    """
    A user is able to favourite an article if thay had not favourited it.
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
            serializer = self.get_serializer(article)
            message = "You have successfully unfavourited this article"
            response = {"message": message, "article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            # Favourites the article
            article.favourited.add(user.id)
            serializer = self.get_serializer(article)
            message = "You have successfully favourited this article"
            response = {"message": message, "article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
