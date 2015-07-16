from django.db import models
import datetime


class SMSVerificationManager(models.Manager):
    def get_queryset(self):
        expiry_datetime = datetime.datetime.now()-datetime.timedelta(minutes=3)
        queryset = super(SMSVerificationManager, self).get_queryset()
        return queryset.filter(datetime__gte=expiry_datetime, is_verified=False)