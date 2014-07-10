# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Min


class Attendance(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.datetime)+ " " +self.user.username

    def get_status(self):
        result = ""
        attend_time = self.user.attendancemanager.get_attend_time()
        leave_time = self.user.attendancemanager.get_leave_time()

        is_first = Attendance.objects.filter(user=self.user, datetime__date=self.datetime.date).aggregate(Min("datetime")).datetime == self.datetime

        if is_first and self.datetime <= attend_time:
            result = "attend"
        elif is_first and self.datetime > attend_time:
            result = "late"
        elif not is_first and self.datetime < leave_time:
            result = "early leave"
        elif not is_first and self.datetime >= leave_time:
            result = "leave"

        return result

#실수로 여러 번 찍을 경우 첫번째와 마지막을 attend와 leave로 하는 게 좋지 않을까(찍지 않고 나가는 경우가 없다고 가정하면)
#그렇게 한다면 is_last도 필요


class AttendanceManager(models.Model):
    user = models.OneToOneField(User)
    group = models.OneToOneField(Group)
    policy = models.ForeignKey("AttendancePolicy")

    def __unicode__(self):
        user = str(self.user) if self.user else ""
        group = str(self.group) if self.group else ""
        return user + group +" policy"

    def get_attend_time(self):
        return self.policy.attend_time

    def get_leave_time(self):
        return self.policy.leave_time


class AttendancePolicy(models.Model):
    attend_time = models.TimeField()
    leave_time = models.TimeField()

    def __unicode__(self):
        return str(self.attend_time) + "/" + str(self.leave_time)
    # def __unicode__(self):
    #     user = str(self.user) if self.user else ""
    #     group = str(self.group) if self.group else ""
    #     return user + group +" policy"
    #
    # def get_attend_time(self):
    #     return self.attend_time
    #
    # def get_leave_time(self):
    #     return self.leave_time