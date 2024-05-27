from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.registration.views import *


# Метаданные Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="VKR",
      default_version='v1',
      description="VKR Polinas",
      terms_of_service="https://app_vkr.com",
      contact=openapi.Contact(email="vkrPolinas@yandex.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('application.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'^account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
            name='account_confirm_email'),

    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/confirmed', VerifyEmailView.as_view(),
            name='email_confirmed'),
    # re_path(r'^account-confirm-email/(<str:key>,)/$', Helper.as_view(),
    #         name='account_confirm_email'),
    #
    # re_path(r'^account-confirm-email/(<str:key>,)/confirmed', VerifyEmailView.as_view(),
    #         name='email_confirmed'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
