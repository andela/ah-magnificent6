from django.urls import path
from .views import (NotificationDetailsView, NotificationAPIView,
                    NotificationSwitchAppAPIView,
                    NotificationSwitchEmailAPIView)

app_name = 'notifications'

urlpatterns = [
    path('<str:pk>', NotificationDetailsView.as_view(), name='notification'),
    path('', NotificationAPIView.as_view(), name='my_notifications'),
    path(
        'switch_app/',
        NotificationSwitchAppAPIView.as_view(),
        name='switch_app_notifications'),
    path(
        'switch_email/',
        NotificationSwitchEmailAPIView.as_view(),
        name='switch_email_notifications'),
]
