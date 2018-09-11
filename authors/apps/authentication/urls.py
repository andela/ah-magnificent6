from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ForgotPasswordAPIView, ResetPasswordAPIView,
    UserActivationAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('user/<int:user_id>', UserRetrieveUpdateAPIView.as_view(),
         name='current_user'),
    path('users/signup/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('accounts/forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot'),
    path('reset_password/<str:token>/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('auth/<str:token>', UserActivationAPIView.as_view(), name='activate_user'),
]
