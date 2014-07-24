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
    image = serializers.ImageField(blank=True)#upload_to="image")

    class Meta:
        model = Attendance
        exclude = ['user', 'group', 'policy']


class AttendanceManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceManager


#class CardResisterSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Card
