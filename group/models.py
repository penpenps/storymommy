# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_superadmin():
    return User.objects.get(is_superuser=True)


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, on_delete=models.SET(get_superadmin))
    create_time = models.DateTimeField(default=timezone.now)

    def create_group(self, name, admin_username):
        admin = User.objects.filter(username=admin_username)
        if len(admin) == 0:
            admin = get_superadmin()
        else:
            admin = admin[0]
        self.create(name=name, admin=admin)

    def check_name_exist(self, name):
        res = self.objects.filter(name=name)
        return len(res) > 0
