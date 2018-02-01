# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from activity_type.models import ActivityType
from volunteer.models import Volunteer
from group.models import get_superadmin


class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)


class TrainingActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.ForeignKey(Training)
    activity_type = models.ForeignKey(ActivityType)
    order = models.IntegerField()


class TrainingRegister(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.ForeignKey(Training)
    volunteer = models.ForeignKey(Volunteer)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)
