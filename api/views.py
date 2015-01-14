# -*- coding: utf-8 -*-

from base64 import b64decode
import uuid
import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from academy.models import Student, Profile
from api.serializer import UserSerializer, StudentSerializer, LoginSerializer, AttendanceSerializer, CardSerializer
from attendance.models import AttendanceManager
from dodream import settings
from dodream.coolsms import send_sms


def get_filename(filename):
    ext = filename.split('.')[-1].lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


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
        academy = self.request.user.profile.staff.academy
        return Student.objects.filter(academy=academy)


class AttendanceCreateAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):


        academy = self.request.user.profile.staff.academy
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            nfc_id = serializer.data['nfc_id']
            image_base64 = request.DATA.get("image_base64")#.replace("\n", "").replace("\r", "").replace(" ", "")
            image = None
            print image_base64
            if image_base64:
                image = ContentFile(b64decode(image_base64))

            profile = Profile.objects.filter(attendancemanager__nfc_id=nfc_id).first()
            if profile and profile.get_academy() == academy:
                serializer.object.profile = profile
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                if image:
                    self.object.image.save(get_filename("image.jpg"), image, save=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                result = {
                    "data": serializer.data,
                    "message": "success",
                    "result": self.object.get_status(),
                    "image": self.object.image.url if image else "no image",
                    "student": StudentSerializer(profile.student).data,
                }
                import sys
                reload(sys)
                sys.setdefaultencoding('utf-8')

                sms_result = 'sms not sent'
                if profile.student:
                    if profile.student.use_sms and profile.student.contact:
                        now = datetime.datetime.now()
                        message = str(unicode(str(now) + " " + profile.student.name + " " + self.object.get_status()))
                        send_sms(message, profile.student.contact)
                        sms_result = 'sms sent'

                result.update({"sms": sms_result})

                return Response(result, headers=headers)
        return Response(serializer.errors)


class CardRegisterAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        academy = self.request.user.profile.staff.academy
        student_id = request.POST.get("student_id")
        nfc_id = request.POST.get("nfc_id")
        force_set = True if request.POST.get("force_set") == "true" else False

        attendance_manager = AttendanceManager.objects.get_or_create(profile__student__id=student_id)[0]
        success, message = attendance_manager.set_nfc(nfc_id, force_set)

        return Response({"success": success, "message": message})


class CardDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        academy = self.request.user.profile.staff.academy
        nfc_id = request.POST.get("nfc_id")
        student = Student.objects.filter(profile__attendancemanager__nfc_id=nfc_id, academy=academy).first()
        student_data = StudentSerializer(student).data if student else None
        return Response({"student": student_data})