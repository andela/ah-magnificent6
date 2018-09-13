from django.urls import path
from .views import ArticleAPIView, ArticleDetailsView, FavoriteArticle

app_name = 'articles'

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='create'),
    path(
        '<str:pk>',
        ArticleDetailsView.as_view(),
        name='retrieveUpdateDelete'),
    path(
        '<str:slug>/favourite/',
        FavoriteArticle.as_view(),
        name='favourite_article'),
]
