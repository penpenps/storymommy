# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from models import Volunteer
from group.models import Group, get_superadmin
from django.db import transaction


def check_volunteer_exist(openid):
    try:
        res = Volunteer.objects.filter(openid=openid)
    except:
        return False
    return len(res) > 0


def create_volunteer(admin_username, openid, name, phone, email, cert_number='', year=0, group_id=None):
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
    Volunteer.objects.create(openid=openid, name=name, phone=phone, email=email, cert_number=cert_number, year=year, group=group, creator=admin)


@transaction.atomic
def update_volunteer_info(openid, name, phone, email, cert_number, year, group_id):
    volunteer = Volunteer.objects.get(openid=openid)
    group = Group.objects.get(id=group_id) if group_id else None
    volunteer.name = name
    volunteer.phone = phone
    volunteer.email = email
    volunteer.cert_number = cert_number
    volunteer.year = year
    volunteer.group = group
    volunteer.save()


def remove_volunteer(openid):
    Volunteer.objects.get(openid=openid).delete()


def check_has_modify_permission(username, openid):
    try:
        user = User.objects.get(username=username)
        if user.is_superuser:
            return True
        v = Volunteer.objects.get(openid=openid)
        if v.group.admin.username == username:
            return True
    except:
        return False
    return False


def get_volunteers_by_group(group_id=None):
    if not group_id:
        return Volunteer.objects.filter(group=None)
    return Volunteer.objects.filter(group__id=group_id)
