from django.urls import path
from .views import ArticleAPIView, ArticleDetailsView


app_name = 'articles'

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name='create'),
    path('articles/<str:pk>', ArticleDetailsView.as_view(),
         name='retrieveUpdateDelete'),
]
