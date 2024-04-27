from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from .serializers import *
# Create your views here.

class RegisterUser(GenericAPIView):
    serializer_class = UserRegisterSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(GenericAPIView):
    serializer_class = UserLoginSerializer  # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]  # определяем тип входных данных

    def post(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            serializer = UserLoginSerializer(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request: Request, *args, **kwargs) -> Response:
    try:
        # Delete the user's token to logout
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@permission_classes([IsAuthenticated])
class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# def change_password(request):
#     if request.method == 'POST':
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if user.check_password(serializer.data.get('old_password')):
#                 user.set_password(serializer.data.get('new_password'))
#                 user.save()
#                 update_session_auth_hash(request, user)  # To update session after password change
#                 return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
#             return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
