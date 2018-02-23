# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from activity.models import Activity
import uuid


class Qrcode(models.Model):
    REGISTER = 0
    SIGN_UP = 1
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField()
    type = models.IntegerField(default=REGISTER)
    activity = models.ForeignKey(Activity, null=True)
    qrcode = models.ImageField(upload_to='static/qrcode', blank=True, null=True)

'''
class OperationRecord(models.Model):
    REGISTER = 0
    ACTIVITY_REGISTER = 1
    ACTIVITY_SIGN_UP = 2
    TRAINING_REGISTER = 3
    ACTIVITY_CREATE = 4
    TRAINING_CREATE = 5
    ACTIVITY_REGISTER_UPDATE = 6

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(default=timezone.now)

'''

