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
from gcm import *
#import gcm
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from academy.models import Student, Profile, Guardian
from api.serializer import UserSerializer, StudentSerializer, LoginSerializer, AttendanceSerializer, CardSerializer
from attendance.models import AttendanceManager
from dodream import settings
# from dodream.coolsms import send_sms


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

                # sms_result = 'sms not sent'
                alert_result = 'alert not sent'
                if profile.student:
                    if profile.student.use_sms:
                        now = datetime.datetime.now()
                        # message = str(unicode(str(now) + " " + profile.student.name + " " + self.object.get_status()))
                        # send_sms(message, profile.student.contact)
                        # sms_result = 'sms sent'
                        alert_result = 'alert sent'

                        # GCM = gcm.GCM
                        gcm = GCM(settings.GCM_APIKEY)
                        data = {'name': profile.get_name(), 'time': now.strftime("%Y년 %m월 %d일 %H:%M:%S"), 'status': "출석 : "}
                        reg_ids = []

                        for guardian in profile.student.guardian_set.all():
                            if guardian.profile.phone_id:
                                reg_ids.append(guardian.profile.phone_id)

                        if reg_ids:
                            gcm.json_request(registration_ids=reg_ids, data=data)

                        result.update({"alert": alert_result, "reg_id": reg_ids})
            return Response(result, headers=headers)
        return Response(serializer.errors)


class CardRegisterAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        academy = self.request.user.profile.staff.academy
        student_id = request.POST.get("student_id")
        nfc_id = request.POST.get("nfc_id")
        force_set = True if request.POST.get("force_set") == "true" else False

        if Profile.objects.filter(student__id=student_id).exists():
            profile = Profile.objects.get(student__id=student_id)
            attendance_manager = AttendanceManager.objects.get_or_create(profile=profile)[0]
            success, message = attendance_manager.set_nfc(nfc_id, force_set)
            return Response({"success": success, "message": "&등록되었습니다."})
        else:
            return Response({"success": False, "message": "&해당학생은 존재하지 않습니다."})

        return Response({"success": success, "message": message})


class CardDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        academy = self.request.user.profile.staff.academy
        nfc_id = request.POST.get("nfc_id")
        student = Student.objects.filter(profile__attendancemanager__nfc_id=nfc_id, academy=academy).first()

        if Profile.objects.filter(student=student).exists():
            student_data = StudentSerializer(student).data
            return Response({"student": student_data})
        else:
            return  Response({"message": "Error! No data"})


class PhoneRegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        phone_id = request.POST.get("phone_id")
        phone_number = request.POST.get("phone_number")

        if Guardian.objects.filter(contact=phone_number).exists():
            guardians = Guardian.objects.filter(contact=phone_number)
            for guardian in guardians:
                guardian.profile.phone_id = phone_id
                guardian.profile.save()
            return Response({"success": "Success", "message": "&기기가 등록 되었습니다. 이제부터 알람을 받아보실 수 있습니다."})
        else:
            return Response({"success": "Fail", "message": "&해당 학부모 휴대폰 번호가 존재하지 않습니다. 폴리니 음악학원에 문의하여 학부모 휴대폰 번호를 등록하세요."})
