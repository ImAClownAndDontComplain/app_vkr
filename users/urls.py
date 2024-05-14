# from django.urls import path, re_path, reverse_lazy, include
# from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from . import views
#
# app_name = "users"
#
# urlpatterns = [
#     path('login/', views.LoginUser.as_view(), name='login'),
#     path('logout/', views.logout_user, name='logout'),
#     path('register/', views.RegisterUser.as_view(), name='register'),
#     path('change-password/', views.ChangePassword.as_view(), name='change_password'),
#     # path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
#     # path('password-reset/',
#     #      PasswordResetView.as_view(
#     #         success_url=reverse_lazy("users:password_reset_done")
#     #      ),
#     #      name='password_reset'),
#     #
#     # path('password-reset/done/',
#     #      PasswordResetDoneView.as_view(),
#     #      name='password_reset_done'),
#     # path('password-reset/<uidb64>/<token>/',
#     #      PasswordResetConfirmView.as_view(
#     #         success_url=reverse_lazy("users:password_reset_complete")
#     #      ),
#     #      name='password_reset_confirm'),
#     # path('password-reset/complete/',
#     #      PasswordResetCompleteView.as_view(),
#     #      name='password_reset_complete'),
# ]

from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    # path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path(r'^account-confirm-email/', VerifyEmailView.as_view(),
    #         name='account_email_verification_sent'),
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
    #         name='account_confirm_email'),
]