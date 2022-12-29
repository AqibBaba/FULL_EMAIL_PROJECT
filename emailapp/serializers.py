from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']


    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer2(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','email','date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68,  write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class EmailVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emails
        fields = ['sender','receiver','subject','compose']

class EmailVerificationSerializer2(serializers.ModelSerializer):

    class Meta:
        model = EmailsSer
        fields = ['sender','receiver','subject','compose']

class NewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField()

class ForgotPassword(serializers.Serializer):
    forgot_password=serializers.CharField()

class ForgetPasswordForUser(serializers.Serializer):
    forgot_password_for_user=serializers.CharField()

class UpdateUserSerializer(serializers.Serializer):
    update=serializers.CharField()