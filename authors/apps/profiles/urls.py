from django.urls import path
from .views import FollowAPIView, FollowersAPIView, FollowingAPIView

app_name = 'profiles'

urlpatterns = [
    path('<username>/follow/', FollowAPIView.as_view(), name='follow'),
    path('<username>/followers/', FollowersAPIView.as_view(), name='followers'),
    path('<username>/following/', FollowingAPIView.as_view(), name='following')
]
