from django.urls import path
from .views import NotificationDetailsView, NotificationAPIView


app_name = 'notifications'

urlpatterns = [
    path(
        '<str:pk>',
        NotificationDetailsView.as_view(),
        name='notification'),
    path(
        '',
        NotificationAPIView.as_view(),
        name='my_notifications'),
]
