# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from group.models import get_superadmin, Group
from volunteer.models import Volunteer
from activity.models import ActivityRegister, Activity
from models import Training, TrainingActivity, TrainingRegister
from activity_type.models import ActivityType
from activity_type.admin import check_activity_type_exist
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q


def check_training_exist(training_id):
    try:
        res = Training.objects.filter(id=training_id)
    except:
        return False
    return len(res) > 0


def check_training_acitivity_exist(ta_id):
    try:
        res = TrainingActivity.objects.filter(id=ta_id)
    except:
        return False
    return len(res) > 0


@transaction.atomic
def create_training(name, activity_type_list, is_private, admin_username, group_id):
    admin = User.objects.filter(username=admin_username)
    if len(admin) == 0:
        admin = get_superadmin()
    else:
        admin = admin[0]
    group = Group.objects.filter(id=group_id).first() if group_id else None
    training = Training.objects.create(name=name, group=group, is_private=is_private, creator=admin)
    for i, at_id in activity_type_list:
        if check_activity_type_exist(at_id):
            at = ActivityType.objects.get(id=at_id)
            TrainingActivity.objects.create(training=training, activity_type=at, order=i)
    return training


@transaction.atomic
def update_training(training_id, name, group_id, is_private, activity_type_update_info):
    training = Training.objects.get(id=training_id)
    training.name = name
    training.group = Group.objects.filter(id=group_id).first()
    training.is_private = is_private
    training.save()
    existed_ta_list = TrainingActivity.objects.filter(training__id=training_id)
    for ta in existed_ta_list:
        if ta.id not in activity_type_update_info:
            ta.delete()
    for ta_id, item in activity_type_update_info.items():
        try:
            training_activity = TrainingActivity.objects.get(id=ta_id)
            ac_type_id = item["activity_type_id"]
            activity_type = ActivityType.objects.filter(id=ac_type_id).first()
            if activity_type:
                training_activity.activity_type = activity_type
            else:
                continue
            training_activity.order = int(item["order"])
            training_activity.save()
        except (TrainingActivity.DoesNotExist, ValidationError):
            ac_type_id = item["activity_type_id"]
            activity_type = ActivityType.objects.filter(id=ac_type_id).first()
            order = int(item["order"])
            TrainingActivity.objects.create(training=training, activity_type=activity_type, order=order)


def remove_training(training_id):
    Training.objects.filter(id=training_id).delete()


def get_privileged_trainings(user):
    if user.is_superuser:
        return Training.objects.all().order_by('-create_time')
    return Training.objects.filter(Q(creator__username=user.username) | Q(group__admin__username=user.username) \
                                       | Q(creator__is_superuser=True, is_private=False, group=None)).order_by('-create_time')


def check_training_modify_permission(username, training_id):
    user = User.objects.get(username=username)
    if user.is_superuser:
        return True
    try:
        training = Training.objects.get(id=training_id)
        if training.creator.username == username or training.group.admin.username == username:
            return True
    except:
        return False
    return False


def get_all_types_as_options(user):
    t_list = get_privileged_trainings(user)
    options = []
    for t in t_list:
        options.append({
            "text": t.name,
            "value": t.id
        })
    return options


def remove_training_activity(ta_id):
    TrainingActivity.objects.filter(id=ta_id).delete()


def get_all_training(user):
    if user.is_superuser:
        trainings = Training.objects.all().order_by('-create_time')
    else:
        trainings = Training.objects.filter(Q(group__admin__username=user.username) | Q(creator__username=user.username)).order_by('-create_time')
    res = []
    for t in trainings:
        res.append(get_training_status(t))

    return res


def get_training_status(t):
    item = {"id": t.id, "name": t.name, "creator": t.creator.first_name, "create_time": t.create_time, "types": []}
    if t.group:
        item['group_id'] = t.group.id
        item['group_name'] = t.group.name
    else:
        item['group_id'] = '-'
        item['group_name'] = u"未分组"
    item["is_private_value"] = t.is_private
    item["is_private"] = u"私密" if t.is_private else u"公开"
    item["count"] = TrainingRegister.objects.filter(training__id=t.id).count()

    for ta in TrainingActivity.objects.filter(training__id=t.id).order_by('order'):
        item["types"].append({
            "id": ta.id,
            "at_id": ta.activity_type.id,
            "at_name": ta.activity_type.name,
            "order": ta.order
        })
    return item


def register_training(training_id, openid, admin_username):
    admin = User.objects.filter(username=admin_username).first()
    admin = get_superadmin() if not admin else admin
    volunteer = Volunteer.objects.get(openid=openid)
    training = Training.objects.get(id=training_id)
    TrainingRegister.objects.create(training=training, volunteer=volunteer, creator=admin)


def get_all_training_register(user, training_id):
    if user.is_superuser:
        registers = TrainingRegister.objects.filter(training__id=training_id).order_by('-create_time')
    else:
        registers = TrainingRegister.objects.filter(training__id=training_id).filter(Q(volunteer__group__admin__username=user.username) | Q(creator__username=user.username)).order_by('-create_time')
    return get_training_registers_status(registers)


def get_volunteer_registers(openid):
    registers = TrainingRegister.objects.filter(volunteer__openid=openid).order_by('-create_time')
    return get_training_registers_status(registers)


def get_training_registers_status(registers):
    res = []
    for r in registers:
        item = {"id": r.id, "openid": r.volunteer.openid, "name": r.volunteer.name, "activity_list": []}
        ta_list = TrainingActivity.objects.filter(training__id=r.training.id).order_by('order')
        for ta in ta_list:
            tmp = {
                "type": ta.activity_type.name,
                "order": ta.order
            }

            activity_register = ActivityRegister.objects.filter(training_activity_mapping__id=ta.id, volunteer__openid=r.volunteer.openid).first()
            tmp['name'] = activity_register.activity.name if activity_register else None
            tmp['status_value'] = activity_register.status if activity_register else None
            tmp['status'] = activity_register.get_status_display() if activity_register else None
            item["activity_list"].append(tmp)
        res.append(item)
    return res


def remove_training_register(register_id):
    TrainingRegister.objects.filter(id=register_id).delete()


def check_training_register_permission(username, training_id, openid):
    user = User.objects.get(username=username)
    if user.is_superuser:
        return True
    # Currently, only system admin can change training register
    return False


def check_training_register_exist(training_id, openid):
    res = TrainingRegister.objects.filter(training__id=training_id, volunteer__openid=openid)
    return len(res) > 0


def get_training_by_activity(activity_id):
    activity = Activity.objects.get(id=activity_id)
    return TrainingActivity.objects.filter(activity_type__id=activity.type.id)

