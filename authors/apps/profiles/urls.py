from django.urls import path
from .views import FollowAPIView, FollowersAPIView, FollowingAPIView, ProfilesAPIView


app_name = 'profiles'

urlpatterns = [
    path('authors/', ProfilesAPIView.as_view(), name='profiles'),
    path('<username>/follow/', FollowAPIView.as_view(), name='follow'),
    path('<username>/followers/', FollowersAPIView.as_view(), name='followers'),
    path('<username>/following/', FollowingAPIView.as_view(), name='following')
]
