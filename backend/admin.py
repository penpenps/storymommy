# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import transaction


@transaction.atomic
def create_user(username, password, name, phone, email=None):
    user = User.objects.create_user(username, email, password)
    user.first_name = name
    user.last_name = phone
    user.save()


@transaction.atomic
def remove_user(username):
    user = User.objects.get(username=username)
    user.delete()

@transaction.atomic
def update_user(username,  name, phone, email):
    user = User.objects.get(username=username)
    user.first_name = name
    user.last_name = phone
    user.email = email
    user.save()


def is_username_valid(user_name):
    try:
        user = User.objects.get(username=user_name)
        return True
    except User.DoesNotExist:
        return False

