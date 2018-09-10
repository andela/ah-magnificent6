"""
This module defines views used in CRUD operations on articles.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .serializers import ArticleSerializer
from django.views.generic import ListView
from rest_framework.views import APIView
from .models import Article
from .renderers import ArticleJSONRenderer


class ArticleAPIView(generics.ListCreateAPIView):
    """
    user generics.CreateAPIView to expose parameters to the documentation
    method: post
    Create a new article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def post(self, request):
        """
        Creates an article
        :params HttpRequest: a post request with article data sent by clients
        to create a new article.
        :return:returns a successfully created article
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
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ArticleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    permission_classes = (IsAuthenticated,)

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
            return Response(
                {
                    'error': 'Article with given id does not exist'
                }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        This method handles request to delete a given article.
        :params pk: an id of the article to be deleted
                request: a request object with authenticated user credentials
        :returns dict: a json object containing message to indicate that the
        article has been deleted
        """
        article = self.get_object(pk)
        if not article:
            # return error message for non-existing article
            return Response(
                {
                    'error': 'Article with given id does not exist'
                }, status.HTTP_404_NOT_FOUND)
        # check whether user owns this article before attempting to delete it
        if article.author.id == request.user.id:
            article.delete()
            return Response(
                {
                    'message': "Article with id={} deleted" .format(int(pk))
                }, status.HTTP_200_OK)
        else:
            # prevent a user from deleting an article s/he does not own
            return Response(
                {
                    'error': 'You cannot delete articles belonging\
                to other users.'
                }, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """
        handle request to update a given article
        :params pk: an id for the article to be updated
                request: a request object with new data for the article
        """
        article = self.get_object(pk)
        if not article:
            # Tell client we have not found the requested article
            return Response(
                {'error': 'Article with given id does not exist'},
                status.HTTP_404_NOT_FOUND)
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
