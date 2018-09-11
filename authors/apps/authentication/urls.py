from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
<<<<<<< HEAD
    ForgotPasswordAPIView, ResetPasswordAPIView
=======
>>>>>>> [Feature #159965302] Implement pull request reviews and update tests after rebase
    UserActivationAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('user/<int:user_id>', UserRetrieveUpdateAPIView.as_view(),
         name='current_user'),
    path('users/signup/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
<<<<<<< HEAD
    path('accounts/forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot'),
    path('reset_password/<str:token>/', ResetPasswordAPIView.as_view(), name='reset_password')
=======
>>>>>>> [Feature #159965302] Implement pull request reviews and update tests after rebase
    path('auth/<str:token>', UserActivationAPIView.as_view(), name='activate_user'),
]
