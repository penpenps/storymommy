# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from models import Volunteer
from common.Utils import format_datetime_str
from common.Result import Result
from common import Consts
from group.admin import get_all_group_as_options, check_group_exist
import admin
import json
import csv
import datetime


@login_required
def volunteer(request):

    data = {
        "pageName": u"志愿者列表"
    }
    return render(request, 'volunteer.html', data)


@login_required
def update_volunteer_info(request):
    result = Result()
    openid = request.POST['openid']
    name = request.POST['name']
    group_id = request.POST['group_id']
    phone = request.POST['phone']
    cert_number = request.POST['cert_number']
    year = request.POST['year']
    if not admin.check_volunteer_exist(openid):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_VOLUNTEER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not admin.check_has_modify_permission(request.user.username, openid):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if group_id != '-' and not check_group_exist(group_id):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_GROUP_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        if group_id == '-':
            admin.update_volunteer_info(openid, name, phone, cert_number, year, None)
        else:
            admin.update_volunteer_info(openid, name, phone, cert_number, year, group_id)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def remove_volunteer(request, openid):
    result = Result()
    if not admin.check_volunteer_exist(openid):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_VOLUNTEER_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    if not admin.check_has_modify_permission(request.user.username, openid):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NO_PERMISSION_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
    try:
        admin.remove_volunteer(openid)
        result.code = Consts.SUCCESS_CODE
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
def load_volunteer_list(request):
    volun_data = []
    if request.user.is_superuser:
        volun_list = Volunteer.objects.all()
    else:
        volun_list = Volunteer.objects.filter(group__admin__username=request.user.username)
    for i, v in enumerate(volun_list):
        item = [{
            "value": v.openid,
            "text": str(i+1)
        }, {
            "value": v.name,
            "text": v.name
        }, {
            "value": v.group.id if v.group else "-",
            "text": v.group.name if v.group else u"未分组"
        }, {
            "value": v.phone,
            "text": v.phone
        }, {
            "value": v.cert_number,
            "text": v.cert_number
        }, {
            "value": v.year,
            "text": v.year
        }, {
            "text": v.creator.first_name
        }, {
            "text": format_datetime_str(v.create_time)
        }
        ]
        volun_data.append(item)

    data = {
        "table": {
            "id": "groupTable",
            "name": u"志愿者列表",
            "label": "group",
            "header": ["ID", u"姓名", u"小组", u"电话", u"工作证号", u"工作年限", u"创建人", u"创建时间"],
            "labels": ["openid", "name", "group_id", "phone", "cert_number", "year", "creator_username", "create_time"],
            "edit": {
                "link": "/volunteer/update_volunteer_info",
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
                        "options": get_all_group_as_options()
                    },
                    {
                        "index": 3,
                        "enable": True,
                        "type": "text"
                    },
                    {
                        "index": 4,
                        "enable": True,
                        "type": "text"
                    },
                    {
                        "index": 5,
                        "enable": True,
                        "type": "number"
                    }
                ]
            },
            "remove": {
                "link": "/volunteer/remove_volunteer/",
                "label": "name",
                "param": "id"
            },
            "body": volun_data
        }
    }
    return render(request, 'table.html', data)


@login_required
def download_volunteer_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="volunteer_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    writer = csv.writer(response)
    header = [u"姓名", u"小组", u"电话", u"工作证号", u"工作年限", u"创建人", u"创建时间"]
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    if request.user.is_superuser:
        volun_list = Volunteer.objects.all()
    else:
        volun_list = Volunteer.objects.filter(group__admin__username=request.user.username)
    for v in volun_list:
        items = [v.name, v.group.name, v.phone, v.cert_number, v.year, v.group.admin.first_name, format_datetime_str(v.create_time)]
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response
