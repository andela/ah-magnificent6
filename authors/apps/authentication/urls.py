from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, 
    ForgotPasswordAPIView, ResetPasswordAPIView, UserActivationAPIView, SocialLoginView
)

app_name = 'authentication'

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view(),
         name='current_user'),
    path('users/signup/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('accounts/forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot'),
    path('reset_password/<str:token>/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('auth/<str:token>', UserActivationAPIView.as_view(), name='activate_user'),
    # social login urls
    path('users/oauth/', SocialLoginView.as_view(), name='social_auth'),
]
