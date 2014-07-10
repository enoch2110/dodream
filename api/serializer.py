from django.contrib.auth.models import User
from rest_framework import serializers
from academy.models import Student


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student