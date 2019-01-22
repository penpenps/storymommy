# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activity_type.admin import get_all_types_as_options, check_activity_type_exist
from volunteer.admin import check_volunteer_exist
from training.admin import get_training_by_activity, check_training_register_exist, check_training_acitivity_exist
from training.models import TrainingActivity
from models import Activity
from common.Utils import format_datetime_str
from common.Result import Result
from common import Consts
import admin
import json
import csv
import datetime
import codecs


@login_required
def activity(request):
    input_items = [
        {
            "name": u"活动名称",
            "label": "name",
            "type": "text"
        },
        {
            "name": u"活动类型",
            "label": "type_id",
            "type": "select",
            "options": get_all_types_as_options(request.user)
        },
        {
            "name": u"起始时间",
            "label": "start_time",
            "type": "datetime"
        }, {
            "name": u"结束时间",
            "label": "end_time",
            "type": "datetime"
        }, {
            "name": u"地址",
            "label": "address",
            "type": "text"
        }
    ]

    data = {
        "pageName": u"活动列表",
        "is_superuser": request.user.is_superuser,
        "add": {
            "label": "activity",
            "link": "/activity/create_activity/",
            "name": u"添加活动",
            "items": input_items
        }
    }
    return render(request, 'activity.html', data)


@login_required
def create_activity(request):
    result = Result()
    name = request.POST['name']
    type_id = request.POST['type_id']
    address = request.POST['address']
    start_time = datetime.datetime.strptime(request.POST['start_time'], Consts.DATETIME_FORMAT)
    end_time = datetime.datetime.strptime(request.POST['end_time'], Consts.DATETIME_FORMAT)
    if start_time >= end_time:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.START_END_TIME_ERROR_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not check_activity_type_exist(type_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_TYPE_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        admin.create_activity(name, type_id, start_time, end_time, address, request.user.username)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def update_activity(request):
    result = Result()
    activity_id = request.POST['id']
    name = request.POST['name']
    type_id = request.POST['type_id']
    address = request.POST['address']
    start_time = datetime.datetime.strptime(request.POST['start_time'], Consts.DATETIME_FORMAT)
    end_time = datetime.datetime.strptime(request.POST['end_time'], Consts.DATETIME_FORMAT)
    # if start_time < datetime.datetime.now():
    #     result.code = Consts.FAILED_CODE
    #     result.msg = Consts.ACTIVITY_END_MSG
    #     return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if start_time >= end_time:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.START_END_TIME_ERROR_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not check_activity_type_exist(type_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_TYPE_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not admin.check_activity_exist(activity_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not admin.check_modify_activity_permission(request.user.username, activity_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        admin.update_activity(activity_id, name, type_id, start_time, end_time, address)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def remove_activity(request, activity_id):
    result = Result()
    if not admin.check_activity_exist(activity_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not admin.check_modify_activity_permission(request.user.username, activity_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        admin.remove_activity(activity_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def load_activity_list(request):
    at_data = []
    for i, at in enumerate(admin.get_privileged_activities(request.user)):
        item = [{
            "value": at.id,
            "text": str(i+1)
        }, {
            "value": at.name,
            "text": at.name,
            "link": "/activity/register_list/%s/" % at.id
        }, {
            "value": at.type.id,
            "text": at.type.name
        }, {
            "value": format_datetime_str(at.start_time),
            "text": format_datetime_str(at.start_time)
        }, {
            "value": format_datetime_str(at.end_time),
            "text": format_datetime_str(at.end_time)
        }, {
            "value": at.address,
            "text": at.address
        }, {
            "text": at.get_status()
        }, {
            "text": admin.get_activity_register_count(at.id)
        }
        ]
        at_data.append(item)

    data = {
        "table": {
            "id": "activityTable",
            "name": u"活动列表",
            "label": "activity",
            "header": ["ID", u"活动名称", u"活动类型", u"起始时间", u"结束时间", u"地址", u"状态", u"注册人数"],
            "labels": ["id", "name", "type_id", "start_time", "end_time", "address", "status", "register_cnt"],
            "edit": {
                "link": "/activity/update_activity",
                "items": [
                    {
                        "index": 0,
                        "enable": False,
                        "type": "text"
                    }, {
                        "index": 1,
                        "enable": True,
                        "type": "text"
                    }, {
                        "index": 2,
                        "enable": True,
                        "type": "select",
                        "options": get_all_types_as_options(request.user)
                    }, {
                        "index": 3,
                        "enable": True,
                        "type": "datetime"
                    }, {
                        "index": 4,
                        "enable": True,
                        "type": "datetime"
                    }, {
                        "index": 5,
                        "enable": True,
                        "type": "text"
                    }
                ]
            },
            "remove": {
                "link": "/activity/remove_activity/",
                "label": "name",
                "param": "id"
            },
            "view": {
                "link": "/activity/register_list/",
                "index": 0
            },
            "body": at_data
        }
    }
    return render(request, 'table.html', data)


@login_required
def download_activity_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activity_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    writer = csv.writer(response)
    header = [u"活动名称", u"活动类型", u"起始时间", u"结束时间", u"地址", u"状态", u"创建者", u"创建时间"]

    writer.writerow([unicode(s).encode("utf-8") for s in header])
    at_list = admin.get_privileged_activities(request.user)
    for at in at_list:
        items = [at.name, at.type.name, format_datetime_str(at.start_time), format_datetime_str(at.end_time), at.address, at.get_status(), at.creator.first_name, format_datetime_str(at.create_time)]
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response


@login_required
def activity_register_list(request, activity_id):
    if not admin.check_activity_exist(activity_id):
        return render(request, 'error.html', {"error_msg": Consts.NOT_FOUND_ACTIVITY_MSG})
    at = Activity.objects.get(id=activity_id)
    data = {
        "pageName": at.name,
        "is_superuser": request.user.is_superuser,
        "activity": at,
        "ta_list": get_training_by_activity(at.id)
    }
    return render(request, 'activity_register.html', data)


@login_required
def load_activity_register_list(request, activity_id):
    register_data = []
    for i, r in enumerate(admin.get_all_register(request.user, activity_id)):
        item = [{
            "text": str(i+1),
            "value": r.id
        }, {
            "text": r.volunteer.name,
            "value": r.volunteer.name
        }, {
            "text": r.get_status_display(),
            "value": r.status
        }, {
            "text": r.creator.first_name
        }, {
            "text": format_datetime_str(r.create_time)
        }, {
            "text": "%s-%d-%s" % (r.training_activity_mapping.training.name, r.training_activity_mapping.order, r.training_activity_mapping.activity_type.name) if r.training_activity_mapping else u"单独活动"
        }]
        if request.user.is_superuser:
            item.append({
                "text": r.volunteer.group.name if r.volunteer.group else "-"
            })
        register_data.append(item)

    data = {
        "table": {
            "id": "activityRegisterTable",
            "name": u"活动注册列表",
            "label": "activity",
            "header": ["ID", u"志愿者", u"状态", u"创建者", u"注册时间", u"关联培训"],
            "labels": ["id", "name", "status", "creator", "create_time", "training"],
            "edit": {
                "link": "/activity/update_activity_register",
                "items": [
                    {
                        "index": 0,
                        "enable": False,
                        "type": "text"
                    },  {
                        "index": 2,
                        "enable": True,
                        "type": "select",
                        "options": admin.get_activity_register_status_as_options()
                    }
                ]
            },
            "remove": {
                "link": "/activity/remove_activity_register/",
                "label": "name",
                "param": "id"
            },
            "body": register_data
        }
    }

    if request.user.is_superuser:
        data["table"]["header"].append(u"小组")
        data["table"]["labels"].append("group_id")

    return render(request, 'table.html', data)


@login_required
def download_activity_register_list(request, activity_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="register_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    # print 'attachment; filename="%s_%s.csv"' % (at.name, datetime.date.today().strftime("%Y_%m_%d"))
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    header = [u"志愿者", u"状态", u"创建者", u"小组", u"注册时间", u"更新时间"]

    writer.writerow([unicode(s).encode("utf-8") for s in header])
    register_list = admin.get_all_register(request.user, activity_id)
    
    for r in register_list:
        items = [r.volunteer.name, r.get_status_display(), r.creator.first_name, r.volunteer.group.name, format_datetime_str(r.create_time), format_datetime_str(r.update_time)]
        writer.writerow([unicode(s).encode("utf-8") if s else '' for s in items])

    return response


@login_required
def register_activity(request):
    activity_id = request.POST['activity_id']
    volun_list = request.POST['volun_list'].split(',')
    is_training = True if request.POST['type'] == 'training' else False
    ta_id = request.POST['ta_id']
    res = {"success": 0, "failed": 0, "msg": {}}
    username = request.user.username
    for v_id in volun_list:
        if not check_volunteer_exist(v_id):
            res["failed"] += 1
            res["msg"][v_id] = Consts.NOT_FOUND_VOLUNTEER_MSG
            continue
        if admin.check_activity_register_exist(activity_id, v_id):
            res["failed"] += 1
            res["msg"][v_id] = Consts.ACTIVITY_REGISTER_EXIST_MSG
            continue
        if not admin.check_register_activity_permission(username, activity_id, v_id):
            res["failed"] += 1
            res["msg"][v_id] = Consts.NO_PERMISSION_MSG
            continue
        try:
            if is_training and check_training_acitivity_exist(ta_id):
                ta = TrainingActivity.objects.get(id=ta_id)
                if not check_training_register_exist(ta.training.id, v_id):
                    res["failed"] += 1
                    res["msg"][v_id] = Consts.NOT_FOUND_TRAINING_REGISTER_MSG
                    continue
                admin.register_activity(activity_id, v_id, username, ta_id)
            else:
                admin.register_activity(activity_id, v_id, username)
            res["success"] += 1
        except:
            res["failed"] += 1
            res["msg"][v_id] = Consts.UNKNOWN_ERROR
            raise
    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def update_activity_register(request):
    result = Result()
    register_id = request.POST['id']
    status = int(request.POST['status'])
    if not admin.check_activity_register_exist_by_id(register_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_REGISTER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_modify_activity_register_permission(request.user.username, register_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        admin.update_activity_register_status(register_id, status)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def remove_activity_register(request, register_id):
    result = Result()
    if not admin.check_activity_register_exist_by_id(register_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_ACTIVITY_REGISTER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    if not admin.check_modify_activity_register_permission(request.user.username, register_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    try:
        admin.remove_activity_register(register_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")