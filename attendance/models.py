# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.db import models


class Attendance(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.datetime)+ " " +self.user.username

    def get_status(self):
        result = ""
        attend_time = self.user.attendancemanager.policy.get_attend_time()
        leave_time = self.user.attendancemanager.policy.get_leave_time()

        is_first = Attendance.objects.filter(user=self.user, datetime__date=self.datetime.date).count() == 1

        if is_first and self.datetime <= attend_time:
            result = "attend"
        elif is_first and self.datetime > attend_time:
            result = "late"
        elif not is_first and self.datetime < leave_time:
            result = "early leave"
        elif not is_first and self.datetime >= leave_time:
            result = "leave"

        return result

#현재 user로 저장된 attendance끼리 비교해서 첫번짼지 확인해야 됨
#어떻게? 모든 attendance의 user를 비교? 시간 순서로 된 attendance 중 해당 user에 대한 첫번째 attendance를 first로? attendace를 생성할 때 first임을 저장?
#실수로 여러 번 찍을 경우 첫번째와 마지막을 attend와 leave로 하는 게 좋지 않을까(찍지 않고 나가는 경우가 없다고 가정하면)
#그렇게 한다면 is_last도 필요


class AttendanceManager(models.Model):
    user = models.OneToOneField(User)
    group = models.OneToOneField(Group)
    policy = models.ForeignKey("AttendancePolicy")


class AttendancePolicy(models.Model):
    attend_time = models.TimeField()
    leave_time = models.TimeField()

    def __unicode__(self):
        user = str(self.user) if self.user else ""
        group = str(self.group) if self.group else ""
        return user + group +" policy"

    def get_attend_time(self):
        return self.attend_time

    def get_leave_time(self):
        return self.leave_time