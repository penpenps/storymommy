# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from group.admin import get_all_group_as_options, check_group_exist
from common.Utils import format_datetime_str
from common.Result import Result
from common import Consts
import admin
import json
import csv
import datetime
import codecs


@login_required
def activity_type(request):
    input_items = [
        {
            "name": u"类型名称",
            "label": "name",
            "type": "text"
        },
        {
            "name": u"积分",
            "label": "score",
            "type": "number"
        },
        {
            "name": u"所属小组",
            "label": "group_id",
            "type": "select",
            "options": get_all_group_as_options(request.user)
        }
    ]
    if request.user.is_superuser:
        input_items.append({
            "name": u"权限",
            "label": "is_private",
            "type": "select",
            "options": [{
                "value": False,
                "text": u"公开"
            }, {
                "value": True,
                "text": u"私密"
            }]
        })
    data = {
        "pageName": u"活动类型列表",
        "is_superuser": request.user.is_superuser,
        "add": {
            "label": "admin",
            "link": "/activity_type/create_activity_type/",
            "name": u"添加活动类型",
            "items": input_items
        }
    }
    return render(request, 'activity_type.html', data)


@login_required
def create_activity_type(request):
    result = Result()
    name = request.POST['name']
    score = request.POST['score']
    group_id = request.POST['group_id'] if 'group_id' in request.POST and request.POST['group_id'] != '-' else None
    is_private = request.POST['is_private'] if 'is_private' in request.POST else False

    if group_id and not check_group_exist(group_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_GROUP_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        admin.create_activity_type(name, score, is_private, request.user.username, group_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def update_activity_type(request):
    result = Result()
    type_id = request.POST['id']
    name = request.POST['name']
    score = request.POST['score']
    group_id = request.POST['group_id'] if 'group_id' in request.POST and request.POST['group_id'] != '-' else None
    is_private = request.POST['is_private'] if 'is_private' in request.POST else False

    if not admin.check_activity_type_exist(type_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_TYPE_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_modify_activity_type_permission(type_id, request.user.username):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if group_id and not check_group_exist(group_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_GROUP_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        admin.update_activity_type(type_id, name, score, is_private, group_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def remove_activity_type(request, type_id):
    result = Result()
    if not admin.check_activity_type_exist(type_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_TYPE_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_modify_activity_type_permission(type_id, request.user.username):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        admin.remove_activity_type(type_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def load_activity_type_list(request):
    at_data = []
    for i, at in enumerate(admin.get_privileged_types(request.user)):
        item = [{
            "value": at.id,
            "text": str(i+1)
        }, {
            "value": at.name,
            "text": at.name
        }, {
            "value": at.score,
            "text": at.score
        }, {
            "value": at.group.id if at.group else "-",
            "text": at.group.name if at.group else u"未分组"
        }, {
            "text": at.creator.first_name
        }, {
            "text": format_datetime_str(at.create_time)
        }
        ]
        if request.user.is_superuser:
            item.append({
                "text": u"私密" if at.is_private else u"公开",
                "value": at.is_private
            })
        at_data.append(item)

    data = {
        "table": {
            "id": "activityTypeTable",
            "name": u"活动类型列表",
            "label": "activity-type",
            "header": ["ID", u"类型名称", u"积分", u"所属小组", u"创建者", u"创建时间"],
            "labels": ["id", "name", "score", "group_id", "creator", "create_time"],
            "edit": {
                "link": "/activity_type/update_activity_type",
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
                        "type": "number"
                    },
                    {
                        "index": 3,
                        "enable": True,
                        "type": "select",
                        "options": get_all_group_as_options(request.user)
                    }
                ]
            },
            "remove": {
                "link": "/activity_type/remove_activity_type/",
                "label": "name",
                "param": "id"
            },
            "body": at_data
        }
    }
    if request.user.is_superuser:
        data['table']['header'].append(u"权限")
        data['table']['labels'].append(u"is_private")
        data['table']['edit']['items'].append({
            "index": 6,
            "enable": True,
            "type": "select",
            "options": [{
                "text": u"私密",
                "value": True
            }, {
                "text": u"公开",
                "value": False
            }]
        })
    return render(request, 'table.html', data)


@login_required
def download_activity_type_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activity_type_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    header = [u"类型名称", u"积分", u"所属小组", u"创建者", u"创建人", u"创建时间"]
    if request.user.is_superuser:
        header.append(u"权限")
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    at_list = admin.get_privileged_types(request.user)
    for at in at_list:
        items = [at.name, at.score, at.group.name if at.group else u"未分组", at.creator.first_name, format_datetime_str(at.create_time)]
        if request.user.is_superuser:
            items.append(u"私密" if at.is_private else u"公开")
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response
