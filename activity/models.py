# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from activity_type.models import ActivityType
from volunteer.models import Volunteer
from training.models import TrainingActivity
from group.models import get_superadmin
from common.Utils import format_datetime_str


class Activity(models.Model):
    NOT_START = u"未开始"
    IN_PROGRESS = u"进行中"
    END = u"已结束"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ActivityType)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    address = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)

    def get_status(self):
        if timezone.now() < self.start_time:
            return self.NOT_START
        if timezone.now() < self.end_time:
            return self.IN_PROGRESS
        return self.END

    def get_start_time(self):
        return format_datetime_str(self.start_time)

    def get_end_time(self):
        return format_datetime_str(self.end_time)

    def get_create_time(self):
        return format_datetime_str(self.create_time)


class ActivityRegister(models.Model):
    REGISTERED = 0
    SIGNED_UP = 1
    ABSENT = 2
    STATUS_CHOICES = (
        (REGISTERED, u"已注册"),
        (SIGNED_UP, u"已签到"),
        (ABSENT, u"缺席")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    volunteer = models.ForeignKey(Volunteer)
    activity = models.ForeignKey(Activity)
    training_activity_mapping = models.ForeignKey(TrainingActivity, on_delete=models.SET(None), default=None, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=REGISTERED)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now, null=True)

