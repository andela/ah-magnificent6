from django.urls import path
from .views import (RetrieveCommentAPIView, ListCreateCommentAPIView,
                    ArticleAPIView, ArticleDetailsView, ArticleLikes, FavoriteArticle,
                    ArticleRatingAPIView, ArticleReportAPIView, ArticleReportRUDAPIView, ArticleBookmarkAPIView, ArticleBookmarkDetailAPIView)

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

    path('<str:slug>/reports', ArticleReportAPIView.as_view(),
         name='reportListCreate'),
    path('<str:slug>/reports/<int:pk>', ArticleReportRUDAPIView.as_view(),
         name='reportRetrieveUpdateDestroy'),

    path('<str:slug>/comments/', ListCreateCommentAPIView.as_view(), name='comments'),
    path('<str:slug>/comments/<pk>/',
         RetrieveCommentAPIView.as_view(), name='comment_detail'),

    path('<str:slug>/comments/<pk>/comments/',
         ListCreateCommentAPIView.as_view()),




    path('<str:slug>/bookmarks/', ArticleBookmarkAPIView.as_view(),
         name='bookmark_article'),
    path('bookmarks/<str:pk>', ArticleBookmarkDetailAPIView.as_view(),
         name='user_bookmarks'),
    path('bookmarks/', ArticleBookmarkDetailAPIView.as_view(),
         name='user_bookmarks')
]
