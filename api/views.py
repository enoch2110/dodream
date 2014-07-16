import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "benchmarks.settings")
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from academy.models import Student
from api.serializer import UserSerializer, StudentSerializer, LoginSerializer, AttendanceSerializer
from attendance.models import AttendanceManager



class Login(generics.RetrieveAPIView):
    """
    Result Code

    0: success
    1: no permission
    2: login failed
    3: login form incorrect
    4: get request not allowed
    """

    serializer_class = LoginSerializer

    def get(self, request):
        result = {"code": "", "message": ""}
        result['code'] = 4
        result['message'] = "get request not allowed"
        return Response(result)

    def post(self, request):
        result = {"code": "", "message": ""}
        account = LoginSerializer(data=request.DATA)
        if account.is_valid():
            username = account.data['username']
            password = account.data['password']
        else:
            result['code'] = 3
            result['message'] = "login form incorrect"
            result.update(account.errors)
            return Response(result)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                result['code'] = 0
                result['message'] = "success"
                result.update({"data": UserSerializer(user).data})
                return Response(result)
            else:
                result['code'] = 1
                result['message'] = "no permission"
        else:
            result['code'] = 2
            result['message'] = "login failed"
        return Response(result)


class StudentListAPI(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'contact')


class AttendanceCreateAPI(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.is_superuser):
            result = {"code": 0, "message": "not authorized"}
            return Response(result)

        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            nfc_id = serializer.data['nfc_id']
            #print User.objects.filter(attendancemanager__nfc_id=nfc_id).exists()
            #if User.objects.filter(attendancemanager__nfc_id=nfc_id).exists():
            serializer.object.user = User.objects.get(attendancemanager__nfc_id=nfc_id)
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            result = self.object.get_status()
            result.update({"data": serializer.data})
            return Response(result, headers=headers)
        return Response(serializer.errors)


# class CardRegisterAPI(generics.CreateAPIView):
#     serializer_class = CardResisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.DATA, files=request.FILES)
#
#         if serializer.is_valid():
#             nfc_id = serializer.data['nfc_id']
#             if not User.objects.filter(attendancemanager__nfc_id=nfc_id).exists():
#
#                 self.pre_save(serializer.object)
#                 self.object = serializer.save(force_insert=True)
#                 self.post_save(self.object, created=True)
#                 headers = self.get_success_headers(serializer.data)
#                 return Response(serializer.data)
#             #else
#
#         return Response(serializer.errors)
