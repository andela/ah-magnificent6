from django.urls import path
<<<<<<< HEAD
from .views import ArticleAPIView, ArticleDetailsView, ArticleRatingAPIView, FavoriteArticle
=======
from .views import (
    ArticleAPIView, ArticleDetailsView, ArticleLikes, FavoriteArticle)
>>>>>>> [feat]: like or dislike an article


app_name = 'articles'

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='create'),
<<<<<<< HEAD
    path('<str:pk>',
         ArticleDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('<str:slug>/favourite/',
         FavoriteArticle.as_view(),
         name='favourite_article'),
    path('<str:pk>', ArticleDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('<str:slug>/rate/', ArticleRatingAPIView.as_view(),
         name='rate'),
=======
    path(
        '<str:slug>',
        ArticleDetailsView.as_view(),
        name='retrieveUpdateDelete'),
    path(
        '<str:slug>/favourite/',
        FavoriteArticle.as_view(),
        name='favourite_article'),
    path('articles/', ArticleAPIView.as_view(), name='create'),
    path('articles/<str:slug>/likes', ArticleLikes.as_view(),
         name='likeArticles'),
>>>>>>> [feat]: like or dislike an article
]
