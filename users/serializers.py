from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)



    # def create(self, validated_data):
    #     user = User(
    #         username=validated_data['username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

# class UserLogoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']
#         # extra_kwargs = {'password': {'write_only': True}}
#
#     # def create(self, validated_data):
#     #     user = User(
#     #         username=validated_data['username'],
#     #         email=validated_data['email']
#     #     )
#     #     user.set_password(validated_data['password'])
#     #     user.save()
#     #     return user
