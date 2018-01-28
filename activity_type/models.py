# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from group.models import Group
from group.models import get_superadmin


class ActivityType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.SET(None), null=True)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)
