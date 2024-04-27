# if user.is_authenticated
#
# # blog_project/settings.py
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'

# path('accounts/', include('accounts.urls')), # новое добавление
#
#
# UNAUTHENTICATED_USER and UNAUTHENTICATED_TOKEN settings.
#
#
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# class ExampleView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # None
#         }
#         return Response(content)



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'email')
#         write_only_fields = ('password',)
#         read_only_fields = ('id',)
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user


# from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
#
#
# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', ]
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def validate_password(self, value):
#         validate_password(value)
#         return value
#
#     def create(self, validated_data):
#         user = get_user_model()(**validated_data)
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user

# from rest_framework import mixins, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
#
# from . import forms, serializers
#
#
# class SignupViewSet(mixins.CreateModelMixin,
#                     viewsets.GenericViewSet):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.SignupSerializer


# @login_required