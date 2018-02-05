# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from group.admin import get_all_group_as_options, check_group_exist
from activity_type.admin import get_all_types_as_options
from common.Utils import format_datetime_str
from common.Result import Result
from common import Consts
import admin
import json
import csv
import datetime


@login_required
def training_list(request):
    input_items = [
        {
            "name": u"培训名称",
            "label": "name",
            "type": "text"
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
        "pageName": u"培训列表",
        "form": {
            "label": "add",
            "link": "/training/create_training/",
            "name": u"添加培训",
            "items": input_items
        },
        "ta_types": get_all_types_as_options(request.user)
    }
    return render(request, 'training.html', data)


@login_required
def create_training(request):
    name = request.POST['name']
    group_id = request.POST['group_id'] if request.POST['group_id'] != '-' else None
    is_private = request.POST['is_private']
    order_list = [int(x) for x in request.POST['order_list'].split(",")]
    ta_list = request.POST['ta_list'].split(',')
    result = Result()
    if group_id and not check_group_exist(group_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_VOLUNTEER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        t = admin.create_training(name, zip(order_list, ta_list), is_private, request.user.username, group_id)
        result.code = Consts.SUCCESS_CODE

    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
        # raise
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def update_training(request):
    training_id = request.POST['training_id']
    name = request.POST['name']
    group_id = request.POST['group_id'] if request.POST['group_id'] != '-' else None
    is_private = request.POST['is_private']
    order_list = [int(x) for x in request.POST['order_list'].split(",")]
    ta_list = request.POST['ta_list'].split(',')
    ta_ids = request.POST['ta_ids'].split(',')
    ta_update_info = {}
    for _id, at_id, order in zip(ta_ids, ta_list, order_list):
        ta_update_info[_id] = {"order": order, "activity_type_id": at_id}
    result = Result()
    if group_id and not check_group_exist(group_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_VOLUNTEER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if training_id and not admin.check_training_exist(training_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_TRAINING_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_training_modify_permission(request.user.username, training_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        t = admin.update_training(training_id, name, group_id, is_private, ta_update_info)
        result.code = Consts.SUCCESS_CODE

    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
        # raise
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def remove_training(request, training_id):
    result = Result()
    if training_id and not admin.check_training_exist(training_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_TRAINING_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_training_modify_permission(request.user.username, training_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        admin.remove_training(training_id)
        result.code = Consts.SUCCESS_CODE

    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
        # raise
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def load_training_list(request):
    trainings = admin.get_all_training(request.user)
    input_items = [
        {
            "name": u"培训名称",
            "label": "name",
            "type": "text"
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
        "training_list": trainings,
        "is_superuser": request.user.is_superuser,
        "form": {
            "label": "edit",
            "link": "/training/update_training/",
            "name": u"修改培训",
            "items": input_items
        },
        "ta_types": get_all_types_as_options(request.user)
    }
    return render(request, 'training_table.html', data)


@login_required
def download_training_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="training_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    writer = csv.writer(response)
    header = [u"培训名称", u"小组", u"创建人", u"创建时间", u"权限", u"活动设置"]
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    trainings = admin.get_all_training(request.user)
    for t in trainings:
        items = [t["name"], t['group_name'], t['creator'], format_datetime_str(t['create_time']), t['is_private']]
        types = [str(x['order'])+"-"+unicode(x['at_name']) for x in t['types']]
        items.append(",".join(types))
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response
