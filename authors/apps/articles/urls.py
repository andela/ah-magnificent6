from django.urls import path
from .views import ArticleAPIView, ArticleDetailsView, ArticleRatingAPIView, FavoriteArticle


app_name = 'articles'

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='create'),
    path('<str:pk>',
         ArticleDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('<str:slug>/favourite/',
         FavoriteArticle.as_view(),
         name='favourite_article'),
    path('articles/', ArticleAPIView.as_view(), name='create'),
    path('articles/<str:pk>', ArticleDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('articles/<str:slug>/rate/', ArticleRatingAPIView.as_view(),
         name='rate'),
]
