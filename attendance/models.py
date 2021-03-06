# -*- coding: utf-8 -*-
from dateutil import tz
import datetime
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Min
from django.utils.timezone import utc
from academy.models import Profile


class Attendance(models.Model):
    profile = models.ForeignKey(Profile)
    image = models.ImageField(upload_to="attendance/attendance", blank=True)
    datetime = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-datetime']

    def __unicode__(self):
        datetime = self.datetime.astimezone(tz.tzlocal())
        username = self.profile.user.username if self.profile.user else "No username"
        return str(datetime.date().isoformat()) + " " + str(datetime.time().isoformat()) + " " + username + " (" + self.get_status() + ")"

    def get_status(self):
        import datetime
        result = ""
        first_attendance = Attendance.objects.filter(profile=self.profile, date=self.date).earliest('datetime')
        is_first = first_attendance == self
        current_datetime = self.datetime.astimezone(tz.tzlocal())
        first_datetime = first_attendance.datetime.astimezone(tz.tzlocal())

        try:
            attend_time = self.profile.attendancemanager.get_attend_time()
            leave_time = self.profile.attendancemanager.get_leave_time()
        except:
            attend_time = first_datetime.time()
            leave_time = (datetime.datetime(2000, 1, 1, attend_time.hour, attend_time.minute, attend_time.second) + datetime.timedelta(hours=1)).time()

        if is_first and current_datetime.time() <= attend_time:
            result = u"출석했습니다."
        elif is_first and current_datetime.time() > attend_time:
            result = u"출석했습니다."
        elif not is_first and current_datetime.time() < leave_time:
            result = u"출석했습니다."
        elif not is_first and current_datetime.time() >= leave_time:
            result = u"출석했습니다."

        return result


class AttendanceManager(models.Model):
    profile = models.OneToOneField(Profile, null=True)
    group = models.OneToOneField(Group, blank=True, null=True)
    policy = models.ForeignKey("AttendancePolicy", blank=True, null=True)
    nfc_id = models.CharField(max_length=50, blank=True, null=True)
    # phone_id = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        profile_name = self.profile.__unicode__() if self.profile else "No Profile"
        return profile_name + " --- " + (self.nfc_id if self.nfc_id else "no nfc card")

    def set_nfc(self, nfc_id, force_set=False):
        #TODO academy specific

        message = ""
        success = False
        if not nfc_id:
            message += "&카드 UID를 확인하세요."
        if self.nfc_id and self.nfc_id != nfc_id:
            message += "&이미 카드를 가지고 있습니다."
        if self.nfc_id and self.nfc_id == nfc_id:
            message += "&해당 카드에 이미 등록되어 있습니다."
        if not self.nfc_id and AttendanceManager.objects.filter(nfc_id=nfc_id).exists():
            message += "&타인이 해당 카드에 등록되어 있습니다."
        if force_set or (not self.nfc_id and not AttendanceManager.objects.filter(nfc_id=nfc_id).exists()):
            AttendanceManager.objects.filter(nfc_id=nfc_id).update(nfc_id=None)
            self.nfc_id = nfc_id
            self.save()
            success = True
            message += "&등록 되었습니다."
        return success, message

    #
    # def set_phone(self, phone_id, force_set=False):
    #
    #     message = ""
    #     success = False
    #     if not phone_id:
    #         message += "&휴대폰 단말기 ID를 확인하세요."
    #     if phone_id:
    #         self.phone_id = phone_id
    #         self.save()
    #         success = True
    #         message += self.profile.student.name + "& 학생의 출석 알람을 받아보실 수 있습니다."
    #     return success, message
    # 
    def get_stu_id(self, nfc):
        user = self.user
        while user:
            if user.nfc == nfc:
                return user.id
            else:
                return 0

    def get_attend_time(self):
        return self.policy.attend_time

    def get_leave_time(self):
        return self.policy.leave_time


class AttendancePolicy(models.Model):
    attend_time = models.TimeField()
    leave_time = models.TimeField()

    def __unicode__(self):
        return str(self.attend_time) + "/" + str(self.leave_time)

import signals