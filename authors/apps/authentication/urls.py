from django.urls import path, include

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, SocialLoginView
)

app_name = 'authentication'

urlpatterns = [
    path('user/<int:user_id>', UserRetrieveUpdateAPIView.as_view(), name='current_user'),
    path('users/signup/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    # social login urls
    path('users/oauth/', SocialLoginView.as_view(), name='social_auth'),
]
