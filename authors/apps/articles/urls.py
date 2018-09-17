from django.urls import path
from .views import (
    ArticleAPIView, ArticleDetailsView, ArticleLikes, FavoriteArticle,
    ArticleRatingAPIView,)


app_name = 'articles'

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='create'),
    path('<str:slug>/rate/', ArticleRatingAPIView.as_view(),
         name='rate'),
    path(
        '<str:slug>',
        ArticleDetailsView.as_view(),
        name='retrieveUpdateDelete'),
    path(
        '<str:slug>/favourite/',
        FavoriteArticle.as_view(),
        name='favourite_article'),
    path('', ArticleAPIView.as_view(), name='create'),
    path('<str:slug>/likes', ArticleLikes.as_view(),
         name='likeArticles'),
]
