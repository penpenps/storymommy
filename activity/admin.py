# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from group.admin import get_superadmin
from models import Activity, ActivityRegister
from training.models import TrainingActivity
from volunteer.models import Volunteer
from volunteer.admin import check_has_modify_permission
from activity_type.models import ActivityType
from activity_type.admin import check_modify_activity_type_permission, get_privileged_types
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum
import json


def create_activity(name, type_id, start_time, end_time, address, admin_username):
    admin = User.objects.filter(username=admin_username)
    if len(admin) == 0:
        admin = get_superadmin()
    else:
        admin = admin[0]

    at = ActivityType.objects.get(id=type_id)

    Activity.objects.create(name=name, type=at, start_time=start_time, end_time=end_time, address=address, creator= admin)


def check_activity_exist(activity_id):
    try:
        res = Activity.objects.filter(id=activity_id)
    except:
        return False
    return len(res) > 0


@transaction.atomic
def update_activity(activity_id, name, type_id, start_time, end_time, address):
    activity = Activity.objects.get(id=activity_id)
    _type = ActivityType.objects.get(id=type_id)
    activity.name = name
    activity.type = _type
    activity.start_time = start_time
    activity.end_time = end_time
    activity.address = address
    activity.save()


def remove_activity(activity_id):
    Activity.objects.get(id=activity_id).delete()


def check_modify_activity_permission(username, activity_id):
    activity = Activity.objects.get(id=activity_id)
    return check_modify_activity_type_permission(activity.type.id, username)


def get_privileged_activities(user):
    privileged_types = [x.id for x in get_privileged_types(user)]
    return Activity.objects.filter(type__id__in=privileged_types).order_by('-create_time')


def check_activity_register_exist(activity_id, openid):
    try:
        res = ActivityRegister.objects.filter(activity__id=activity_id, volunteer__openid=openid)
    except:
        return False
    return len(res) > 0


def check_activity_register_exist_by_id(register_id):
    try:
        res = ActivityRegister.objects.filter(id=register_id)
    except:
        return False
    return len(res) > 0


def get_all_register(user, activity_id):
    if user.is_superuser:
        return ActivityRegister.objects.filter(activity__id=activity_id).order_by('-create_time')
    else:
        return ActivityRegister.objects.filter(activity__id=activity_id).\
            filter(Q(volunteer__group__admin__username=user.username) | Q(creator__username=user.username)).order_by('-create_time')


def register_activity(activity_id, openid, admin_username, training_activity_id=None):
    activity = Activity.objects.get(id=activity_id)
    volunteer = Volunteer.objects.get(openid=openid)
    admin = User.objects.filter(username=admin_username)
    if len(admin) == 0:
        admin = get_superadmin()
    else:
        admin = admin[0]
    if not training_activity_id:
        ActivityRegister.objects.create(activity=activity, volunteer=volunteer, creator=admin)
    else:
        training_activity = TrainingActivity.objects.get(id=training_activity_id)
        ActivityRegister.objects.create(activity=activity, volunteer=volunteer, creator=admin, training_activity_mapping=training_activity)


def check_register_activity_permission(username, activity_id, openid):
    user = User.objects.get(username=username)
    if user.is_superuser:
        return True
    if check_modify_activity_permission(username, activity_id) and check_has_modify_permission(username, openid):
        return True
    return False


def update_activity_register_status(register_id, status):
    register = ActivityRegister.objects.get(id=register_id)
    register.status = status
    register.update_time = timezone.now()
    register.save()


def remove_activity_register(register_id):
    ActivityRegister.objects.get(id=register_id).delete()


def check_modify_activity_register_permission(username, register_id):
    user = User.objects.get(username=username)
    if user.is_superuser:
        return True
    register = ActivityRegister.objects.get(id=register_id)
    if register.volunteer.group.admin.username == username or register.creator.username == username:
        return True
    return False


def get_activity_register_status_as_options():
    options = []
    for value, text in ActivityRegister.STATUS_CHOICES:
        options.append({
            "text": text,
            "value": value
        })
    return options


def get_activity_register_count(activity_id):
    return ActivityRegister.objects.filter(activity__id=activity_id).count()


def get_volunteer_score(openid):
    res = ActivityRegister.objects.filter(volunteer__openid=openid, status=ActivityRegister.SIGNED_UP).aggregate(total_score=Sum('activity__type__score'))
    return res["total_score"] if len(res) > 0 and res["total_score"] else 0