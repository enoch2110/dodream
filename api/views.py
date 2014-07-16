from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from academy.models import Student
from api.serializer import UserSerializer, StudentSerializer, LoginSerializer, AttendanceSerializer
from dodream import settings


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
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'contact')

    def get_queryset(self):
        return Student.objects.filter(academy=self.request.user.staff.academy)


class AttendanceCreateAPI(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.is_superuser):
            result = {"code": 0, "message": "not authorized"}
            return Response(result)

        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            result = {}
            nfc_id = serializer.data['nfc_id']
            if User.objects.filter(attendancemanager__nfc_id=nfc_id).exists():
                user = User.objects.get(attendancemanager__nfc_id=nfc_id)
                serializer.object.user = user

                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                result = {"data": serializer.data, "message": "success", "result": self.object.get_status()}
                return Response(result, headers=headers)
        return Response(serializer.errors)
