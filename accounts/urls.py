from django.urls import path
from .views import *
from .social_auth import GoogleLoginView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from .dashboard_views import DashboardView
from .admin_view import AdminView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='registration'),
    path('auth/active/user/', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/resend/code/', ResendCodeView.as_view(), name='resend_code'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='access_token'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path("auth/account-delete/", DeleteAccountView.as_view(), name="account-delete"),
    # for admin
    path('auth/users/', UserListView.as_view(), name='user_list'),
    path('auth/user/details/', CurrentUserView.as_view(), name='current_user'),
    path('auth/users/<int:pk>/', UserDetailsUpdateView.as_view(), name='user_details_update'),
    path('auth/users/update/', UserUpdateView.as_view(), name='user_update'),
    path('auth/users/activate/<int:id>/', UserActivateView.as_view(), name='user_activate'),
    
        # for social login
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    # path('auth/apple/', AppleLoginView.as_view(), name='apple_login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    
    # for admin user management
    path('admin/users/', AdminView.as_view(), name='admin_user_management'),
]