from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # Registration
    path('registration/', views.RegistrationAPIView.as_view(),name='registration'),
    
    # Activation
    path('activation/confirm/<str:token>', views.ActivationAPIView.as_view(),name='activation'),

    # Activation resend
    path('activation/resend/', views.ActivationResendAPIView.as_view(),name='activation-resend'),

    # Change password
    path('change-password/', views.ChangePasswordAPIView.as_view(),name='change-password'),

    # Reset password
    path('password-reset/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    # Login token
    path('token/login/', views.CustomObtainAuthToken.as_view(),name='activation'),
    path('token/logout/',views.CustomDiscradAuthToken.as_view(),name='token-logout'),
    
    # Login jwt
    path('jwt/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
