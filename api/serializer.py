from django.contrib.auth.models import User
from rest_framework import serializers
from academy.models import Student
from attendance.models import Attendance, AttendanceManager


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student


class AttendanceSerializer(serializers.ModelSerializer):
    nfc_id = serializers.CharField()

    class Meta:
        model = Attendance
        exclude = ['profile']


class AttendanceManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceManager


class CardSerializer(serializers.Serializer):
    class Meta:
        model = AttendanceManager
        fields = ['nfc_id']