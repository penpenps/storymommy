# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from activity.models import Activity
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
import qrcode
import StringIO
import uuid
import qrcode.image.svg

class Qrcode(models.Model):
    REGISTER = 0
    SIGN_UP = 1
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET(None))
    create_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField()
    type = models.IntegerField(default=REGISTER)
    activity = models.ForeignKey(Activity, null=True)
    qrcode = models.ImageField(upload_to='static/qrcode', blank=True, null=True)


