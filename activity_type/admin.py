# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import ActivityType
from group.models import get_superadmin, Group
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q


def check_activity_type_exist(type_id):
    try:
        res = ActivityType.objects.filter(id=type_id)
    except:
        return False
    return len(res)


def create_activity_type(name, score, is_private, admin_username, group_id):
    admin = User.objects.filter(username=admin_username)
    if len(admin) == 0:
        admin = get_superadmin()
    else:
        admin = admin[0]
    group = None
    if group_id:
        groups = Group.objects.filter(id=group_id)
        if len(groups) > 0:
            group = groups[0]
    ActivityType.objects.create(name=name, score=score, is_private=is_private, creator=admin, group=group)


@transaction.atomic
def update_activity_type(type_id, name, score, is_private, group_id):
    at = ActivityType.objects.get(id=type_id)
    group = Group.objects.get(id=group_id) if group_id else None
    at.name = name
    at.score = score
    at.is_private = is_private
    at.group = group
    at.save()


def remove_activity_type(type_id):
    ActivityType.objects.get(id=type_id).delete()


def check_modify_activity_type_permission(type_id, username):
    try:
        admin = User.objects.get(username=username)
        if admin.is_superuser:
            return True
        at = ActivityType.objects.get(id=type_id)
        if at.group.admin.username == username or at.creator.username == username:
            return True
    except:
        return False
    return False


def get_privileged_types(user):
    if user.is_superuser:
        return ActivityType.objects.all()
    return ActivityType.objects.filter(Q(creator__username=user.username) | Q(group__admin__username=user.username) | Q(creator__is_superuser=True, is_private=False))