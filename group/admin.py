# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from models import get_superadmin, Group


def create_group(name, admin_username):
    admin = User.objects.filter(username=admin_username)
    if len(admin) == 0:
        admin = get_superadmin()
    else:
        admin = admin[0]
    Group.objects.create(name=name, admin=admin)


def check_name_exist(name, _id=None):
    if _id:
        res = Group.objects.filter(name=name).exclude(id=_id)
    else:
        res = Group.objects.filter(name=name)
    return len(res) > 0


def check_group_exist(_id):
    try:
        res = Group.objects.filter(id=_id)
    except:
        return False
    return len(res) > 0


@transaction.atomic
def update_group_info(_id, name, admin_username):
    try:
        admin = User.objects.get(username=admin_username)
        group = Group.objects.get(id=_id)
        group.name = name
        group.admin = admin
        group.save()
    except Group.DoesNotExist:
        return None


def remove_group(_id):
    Group.objects.get(id=_id).delete()


def get_all_groups(admin_username=None):
    if admin_username:
        return Group.objects.filter(admin__username=admin_username)
    else:
        return Group.objects.all()


def get_all_admin_as_options():
    options = []
    admins = User.objects.all()
    for u in admins:
        options.append({'value': u.username, 'text': u.first_name})
    return options


def get_all_group_as_options():
    options = [{
        "value": "-",
        "text": u"未分组"
    }]
    groups = Group.objects.all()
    for g in groups:
        options.append({'value': g.id, 'text': g.name})
    return options