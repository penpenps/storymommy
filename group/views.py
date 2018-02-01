# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from volunteer.models import Volunteer
from admin import get_all_groups, get_all_admin_as_options, create_group, check_name_exist, update_group_info as update_group, check_group_exist, remove_group as r_group, get_all_group_as_options
from common.Utils import format_datetime_str
from common.Result import Result
from common import Consts
from models import Group
import json
import csv
import datetime


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def group(request):

    data = {
        "pageName": u"小组列表",
        "add": {
            "label": "admin",
            "link": "/group/add_group",
            "name": u"添加小组",
            "items": [
                {
                    "name": u"小组名称",
                    "label": "name",
                    "type": "text"
                },
                {
                    "name": u"小组管理员",
                    "label": "admin_username",
                    "type": "select",
                    "options": get_all_admin_as_options()
                }
            ]
        }
    }
    return render(request, 'group.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def add_group(request):
    name = request.POST['name']
    admin_username = request.POST['admin_username']
    result = Result()
    if check_name_exist(name):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.GROUP_EXISTED_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        create_group(name, admin_username)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def update_group_info(request):
    _id = request.POST['id']
    name = request.POST['name']
    admin_username = request.POST['admin_username']
    result = Result()
    if check_name_exist(name, _id=_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.GROUP_EXISTED_MSG
    elif not check_group_exist(_id):
        request.code = Consts.FAILED_CODE
        request.msg = Consts.NOT_FOUND_GROUP_MSG
    else:
        try:
            update_group(_id, name, admin_username)
            result.code = Consts.SUCCESS_CODE
        except Exception as e:
            result.code = Consts.FAILED_CODE
            result.msg = Consts.UNKNOWN_ERROR

    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def remove_group(request, _id):
    result = Result()
    if not check_group_exist(_id):
        request.code = Consts.FAILED_CODE
        request.msg = Consts.NOT_FOUND_GROUP_MSG
    else:
        try:
            r_group(_id)
            result.code = Consts.SUCCESS_CODE
        except:
            result.code = Consts.FAILED_CODE
            result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def get_group_list(request):
    return HttpResponse(json.dumps(get_all_group_as_options(request.user)), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def load_group_list(request):
    group_data = []
    for i, g in enumerate(get_all_groups()):
        item = [{
            "value": g.id,
            "text": str(i+1)
        }, {
            "value": g.name,
            "text": g.name
        }, {
            "value": g.admin.username,
            "text": g.admin.first_name
        }, {
            "text": Volunteer.objects.filter(group__id=g.id).count()
        }, {
            "text": format_datetime_str(g.create_time)
        }
        ]
        group_data.append(item)

    data = {
        "table": {
            "id": "groupTable",
            "name": u"小组列表",
            "label": "group",
            "header": ["ID", u"小组名称", u"组长", u"人数", u"创建时间"],
            "labels": ["id", "name", "admin_username", "cnt", "create_time"],
            "edit": {
                "link": "/group/update_group_info",
                "items": [
                    {
                        "index": 0,
                        "enable": False,
                        "type": "text"
                    },
                    {
                        "index": 1,
                        "enable": True,
                        "type": "text"
                    },
                    {
                        "index": 2,
                        "enable": True,
                        "type": "select",
                        "options": get_all_admin_as_options()
                    }
                ]
            },
            "remove": {
                "link": "/group/remove_group/",
                "label": "name",
                "param": "id"
            },
            "body": group_data
        }
    }
    return render(request, 'table.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def download_group_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="group_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    writer = csv.writer(response)
    header = [u"小组名称", u"组长", u"人数", u"创建时间"]
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    groups = Group.objects.all()
    for g in groups:
        items = [g.name, g.admin.first_name, Volunteer.objects.filter(group__id=g.id).count(), format_datetime_str(g.create_time)]
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response

