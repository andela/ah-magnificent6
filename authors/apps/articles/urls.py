from django.urls import path
from .views import ArticleAPIView, ArticleRetrieveUpdateDestroy


app_name = 'articles'

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name='create'),
    path('articles/<str:pk>', ArticleRetrieveUpdateDestroy.as_view(),
         name='retrieveUpdateDelete'),
]
