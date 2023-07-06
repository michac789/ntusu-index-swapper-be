from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from sso import views


app_name = 'sso'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('email-test/', views.EmailTestView.as_view(), name='email-test'),

    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user'),
    path('verify/', views.UserVerifyView.as_view(), name='verify'),
    path('change_password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('forgot_password/', views.ForgotPasswordView.as_view(),
         name='forgot_password'),
]
