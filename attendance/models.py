# -*- coding: utf-8 -*-
from dateutil import tz

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Min
from django.utils.timezone import utc


class Attendance(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField()

    def __unicode__(self):
        datetime = self.datetime.astimezone(tz.tzlocal())
        return str(datetime.date().isoformat()) + " " + str(datetime.time().isoformat()) + " " +self.user.username + " (" + self.get_status() + ")"

    def get_status(self):
        import datetime
        result = ""
        first_attendance = Attendance.objects.filter(user=self.user).earliest('datetime')
        current_datetime = self.datetime.astimezone(tz.tzlocal())
        first_datetime = first_attendance.datetime.astimezone(tz.tzlocal())
        is_first = first_attendance == self

        try:
            attend_time = self.user.attendancemanager.get_attend_time()
            leave_time = self.user.attendancemanager.get_attend_time()
        except:
            attend_time = first_datetime.time()
            leave_time = (datetime.datetime(2000, 1, 1, attend_time.hour, attend_time.minute, attend_time.second) + datetime.timedelta(hours=1)).time()

        print attend_time
        print leave_time

        if is_first and current_datetime.time() <= attend_time:
            result = "attend"
        elif is_first and current_datetime.time() > attend_time:
            result = "late"
        elif not is_first and current_datetime.time() < leave_time:
            result = "early leave"
        elif not is_first and current_datetime.time() >= leave_time:
            result = "leave"

        return result


class AttendanceManager(models.Model):
    user = models.OneToOneField(User)
    group = models.OneToOneField(Group)
    policy = models.ForeignKey("AttendancePolicy")
    nfc_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nfc_id

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
