# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from models import Volunteer
from common.Utils import format_datetime_str, get_openid, get_random_str, get_absolute_url, generate_qrcode
from common.Result import Result
from common import Consts
from common.Decorators import wechat_auth_required
from group.admin import get_all_group_as_options, check_group_exist, get_all_groups
from activity.admin import get_volunteer_score, check_activity_exist, update_activity_register_status, check_activity_register_exist
from activity.models import Activity, ActivityRegister
from training.models import TrainingActivity, TrainingRegister
from training.admin import get_training_registers_status
from backend.models import Qrcode
import admin
import json
import csv
import datetime
from collections import defaultdict


@login_required
def volunteer(request):

    data = {
        "pageName": u"志愿者列表",
        "is_superuser": request.user.is_superuser
    }
    return render(request, 'volunteer.html', data)


@login_required
def volunteer_profile(request, openid):
    if not admin.check_volunteer_exist(openid):
        return render(request, 'error.html', {"error_msg": Consts.NOT_FOUND_VOLUNTEER_MSG})
    if not admin.check_has_modify_permission(request.user.username, openid):
        return render(request, 'error.html', {"error_msg": Consts.NO_PERMISSION_MSG})
    return render(request, 'volunteer_profile.html', get_volunteer_profile(openid))


def get_volunteer_profile(openid):
    activities = ActivityRegister.objects.filter(volunteer__openid=openid).order_by('-create_time')
    activity_payload = []
    for at in activities:
        activity_payload.append({
            "name": at.activity.name,
            "link": "/activity/register_list/%s/" % at.activity.id,
            "time": format_datetime_str(at.activity.start_time) + " - " + format_datetime_str(at.activity.end_time),
            "address": at.activity.address,
            "status_value": at.status,
            "status": at.get_status_display()
        })

    trainings = TrainingRegister.objects.filter(volunteer__openid=openid).order_by('-create_time')
    training_payload = []
    if len(trainings) > 0:
        for t in trainings:
            item = {
                "training_name": t.training.name,
                "link": "/training/register_list/%s/" % t.training.id
            }
            tmp_status = get_training_registers_status([t])[0]
            item.update(tmp_status)
            item['status'] = 0
            start_at_cnt = 0
            for at in item['activity_list']:
                if at['status_value'] > 0:
                    start_at_cnt += 1
            if start_at_cnt < len(item['activity_list']):
                item['status'] = 1
            else:
                item['status'] = 2
            training_payload.append(item)

    data = {
        "volunteer": Volunteer.objects.get(openid=openid),
        "activity_list": activity_payload,
        "training_list": training_payload
    }
    return data


@login_required
def update_volunteer_info(request):
    result = Result()
    openid = request.POST['openid']
    name = request.POST['name']
    group_id = request.POST['group_id']
    phone = request.POST['phone']
    email = request.POST['email']
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
            admin.update_volunteer_info(openid, name, phone, email, cert_number, year, None)
        else:
            admin.update_volunteer_info(openid, name, phone, email, cert_number, year, group_id)
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
        volun_list = Volunteer.objects.all().order_by('-create_time')
    else:
        volun_list = Volunteer.objects.filter(group__admin__username=request.user.username).order_by('-create_time')
    for i, v in enumerate(volun_list):
        item = [{
            "value": v.openid,
            "text": str(i+1)
        }, {
            "value": v.name,
            "text": v.name,
            "link": "/volunteer/volunteer_profile/%s/" % str(v.openid)
        }, {
            "value": v.group.id if v.group else "-",
            "text": v.group.name if v.group else u"未分组"
        }, {
            "value": v.phone,
            "text": v.phone
        }, {
            "value": v.email,
            "text": v.email
        }, {
            "value": v.cert_number,
            "text": v.cert_number
        }, {
            "value": v.year,
            "text": v.year
        }, {
            "text": get_volunteer_score(v.openid)
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
            "header": ["ID", u"姓名", u"小组", u"电话", u"Email", u"工作证号", u"工作年限", u"积分", u"创建人", u"创建时间"],
            "labels": ["openid", "name", "group_id", "phone", "email", "cert_number", "year", "score", "creator_username", "create_time"],
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
                        "options": get_all_group_as_options(request.user)
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
                        "type": "text"
                    },
                    {
                        "index": 6,
                        "enable": True,
                        "type": "number"
                    }
                ]
            },
            "remove": {
                "link": "/volunteer/remove_volunteer/",
                "label": "name",
                "param": "openid"
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
    header = [u"姓名", u"小组", u"电话", u"Email", u"工作证号", u"工作年限", u"创建人", u"创建时间"]
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    if request.user.is_superuser:
        volun_list = Volunteer.objects.all()
    else:
        volun_list = Volunteer.objects.filter(group__admin__username=request.user.username)
    for v in volun_list:
        items = [v.name, v.group.name if v.group else u"未分组", v.phone, v.email, v.cert_number, v.year, v.creator.first_name, format_datetime_str(v.create_time)]
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response


@login_required
def get_volunteer_list(request):
    group_list = request.POST['group_list'].split(",")
    username = request.user.username
    res = defaultdict(list)
    for group_id in group_list:
        volun_list = admin.get_volunteers_by_group(group_id if group_id != '-' else None)
        print volun_list
        for v in volun_list:
            if admin.check_has_modify_permission(username, v.openid):
                res[group_id].append({
                    "text": v.name,
                    "value": str(v.openid)
                })
    return HttpResponse(json.dumps(res), content_type="application/json")


@wechat_auth_required
def register(request, qrcode_id):
    code = request.GET["code"]
    openid = get_openid(code)
    # openid = get_random_str()
    if admin.check_volunteer_exist(openid):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.VOLUNTEER_EXIST_MSG})
    return render(request, 'register.html', {
        "pageName": u'"故事妈妈"志愿者注册',
        "qrcode_id": qrcode_id,
        "openid": openid
    })


@wechat_auth_required
def signup(request, activity_id):
    code = request.GET["code"]
    openid = get_openid(code)
    # openid = "vziO4SeF"
    if not admin.check_volunteer_exist(openid):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.NOT_FOUND_VOLUNTEER_MSG})
    if not check_activity_exist(activity_id):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.NOT_FOUND_ACTIVITY_MSG})
    if not check_activity_register_exist(activity_id, openid):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.NOT_FOUND_ACTIVITY_REGISTER_MSG})
    activity = Activity.objects.get(id=activity_id)
    if activity.start_time > datetime.datetime.now() + datetime.timedelta(hours=1):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.ACTIVITY_NOT_START_MSG})
    if activity.end_time < datetime.datetime.now() - datetime.timedelta(hours=1):
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.ACTIVITY_REG_END_MSG})
    reg = ActivityRegister.objects.get(activity__id=activity_id, volunteer__openid=openid)
    if reg.training_activity_mapping:
        ta = reg.training_activity_mapping
        pre_tas = TrainingActivity.objects.filter(training__id=ta.training.id, order__lt=ta.order)
        for p in pre_tas:
            print p.training.name, p.activity_type.name, ta.order, p.order
            pre_reg = ActivityRegister.objects.filter(training_activity_mapping__id=p.id, volunteer__openid=openid).first()
            if not pre_reg or pre_reg.status != ActivityRegister.SIGNED_UP:
                return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.PRE_ACTIVITIES_ABSENT_MSG})
    if reg.status == ActivityRegister.SIGNED_UP:
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.ACTIVITY_SIGNUP_EXIST_MSG})
    update_activity_register_status(reg.id, ActivityRegister.SIGNED_UP)
    return render(request, 'mobile_callback.html', {"type": "success", "content": u"签到成功。"})


def mobile_error(request):
    return render(request, 'mobile_callback.html', {"type": "danger", "content": u"发生未知系统错误。"})


def register_volunteer(request):
    openid = request.POST['openid']
    qrcode_id = request.POST['qrcode_id']
    email = request.POST['email']
    name = request.POST['name']
    phone = request.POST['phone']
    cert_number = request.POST['cert-number']
    year = request.POST['year']

    result = Result()
    if admin.check_volunteer_exist(openid):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.VOLUNTEER_EXIST_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    qr = Qrcode.objects.filter(id=qrcode_id).first()
    if not qr:
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.QR_NOT_FOUND_MSG})
    if qr.expire_time < datetime.datetime.now():
        return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.EXPIRED_QRCODE_MSG})

    user = qr.creator
    group_id = None
    if not user.is_superuser and len(get_all_groups(user.username)) > 0:
        group_id = get_all_groups(user.username).first().id

    try:
        admin.create_volunteer(user.username, openid, name, phone, email, cert_number, year, group_id)
        return render(request, 'mobile_callback.html', {"type": "success", "content": u"注册成功"})
    except:
        result.code = Consts.FAILED_CODE
    return render(request, 'mobile_callback.html', {"type": "danger", "content": Consts.UNKNOWN_ERROR})


@login_required
def get_qrcode(request):
    result = Result()
    if 'type' not in request.GET:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_GIVEN_QRCODE_TYPE_MSG
        return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

    activity_id = request.GET['activity_id'] if 'activity_id' in request.GET else None
    _type = Qrcode.REGISTER if request.GET['type'] == 'register' else Qrcode.SIGN_UP
    try:
        username = request.user.username
        if request.GET['type'] == 'register':
            qr = Qrcode.objects.filter(creator__username=username, type=_type, expire_time__gt=datetime.datetime.now()).first()
            if not qr:
                expire_time = datetime.datetime.now() + datetime.timedelta(days=7)
                qr = Qrcode.objects.create(creator=request.user, type=Qrcode.REGISTER, expire_time=expire_time)
        else:
            if not check_activity_exist(activity_id):
                result.code = Consts.FAILED_CODE
                result.msg = Consts.NOT_GIVEN_QRCODE_TYPE_MSG
                return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
            qr = Qrcode.objects.filter(creator__username=username, type=_type, activity__id=activity_id, expire_time__gt=datetime.datetime.now()).first()
            if not qr:
                expire_time = datetime.datetime.now() + datetime.timedelta(days=7)
                activity = Activity.objects.get(id=activity_id)
                qr = Qrcode.objects.create(creator=request.user, type=Qrcode.SIGN_UP, expire_time=expire_time, activity=activity)
        url = request.build_absolute_uri(get_absolute_url(qr.id))
        print url
        img = generate_qrcode(url)
        response = HttpResponse(content_type='image/svg+xml')
        img.save(response)
        return response
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
        # raise
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
