# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from group.models import Group
from django.contrib.auth.models import User
from group.models import get_superadmin
from django.utils import timezone


class Volunteer(models.Model):
    openid = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=16)
    email = models.EmailField(max_length=50, default="")
    cert_number = models.CharField(max_length=50, default='')
    year = models.FloatField(default=0, max_digits=4, decimal_places=1)
    group = models.ForeignKey(Group, on_delete=models.SET(None), null=True)
    creator = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)
