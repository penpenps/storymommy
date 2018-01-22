# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import csv
import codecs
import datetime

from django.contrib.auth import authenticate, login as _login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction

from common import Consts
from common.Utils import format_datetime_str
from common.Result import *
from admin import is_username_valid, create_user, update_user, remove_user


@login_required
def index(request):
    data = {
        "pageName": "首页"
    }
    return render(request, 'index.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def admin(request):
    data = {
        "pageName": "管理员",
        "batchload":{
            "label": "admin",
            "link": "/backend/upload_batch_admin"
        }
    }
    return render(request, 'administrators.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def load_admin_list(request):
    users = User.objects.all()
    user_data = []
    for u in users:
        item = [u.username, u.first_name, u.email, u.last_name, format_datetime_str(u.date_joined), format_datetime_str(u.last_login)]
        user_data.append(item)

    data = {
        "table": {
            "id": "adminTable",
            "name": u"小组管理员列表",
            "label": "admin",
            "header": [u"用户名", u"姓名", u"Email", u"手机", u"创建时间", u"最后登入"],
            "labels": ["username", "name", "email", "phone", "create_time", "last_login"],
            "key": 0,
            "edit": {
                "link": "/backend/update_admin_info",
                "items": [0, 1, 2, 3],
                "enable": [1, 2, 3]
            },
            "remove": {
                "link": "/backend/remove_admin/",
                "label": "name"
            },
            "body": user_data
        }
    }
    return render(request, 'table.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def update_admin_info(request):
    username = request.POST['username']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    result = Result()
    try:
        update_user(username, name, phone, email)
        result.code = Consts.SUCCESS_CODE
    except User.DoesNotExist:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_USER_MSG
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def download_admin_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="admin_list_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['username', 'name', 'email', 'phone'])
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def download_admin_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="admin_list_%s.csv"' % datetime.date.today().strftime("%Y_%m_%d")
    writer = csv.writer(response)
    header = [u"用户名", u"姓名", 'email', u"电话", u"创建时间", u"最后登入"]
    writer.writerow([unicode(s).encode("utf-8") for s in header])
    users = User.objects.all()
    for u in users:
        items = [u.username, u.first_name, u.email, u.last_name, format_datetime_str(u.date_joined), format_datetime_str(u.last_login)]
        writer.writerow([unicode(s).encode("utf-8") for s in items])

    return response


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def upload_batch_admin(request):
    result = Result()
    try:
        csv_file = request.FILES.get("uploadInputFile")
        if not csv_file.name.endswith('.csv'):
            result.code = Consts.FAILED_CODE
            result.msg = Consts.INVALID_CSV_FILE_MSG
            return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
        if csv_file.multiple_chunks():
            result.code = Consts.FAILED_CODE
            result.msg = Consts.TOO_LARGE_FILE_MSG
            return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")
        reader = csv.DictReader(codecs.EncodedFile(csv_file, "utf-8"))
        success_count = 0
        failed_count = 0
        failed_idx = []
        failed_reason = []
        for i, row in enumerate(reader):
            username = row['username']
            name = row['name']
            phone = row['phone']
            email = row['email']
            if is_username_valid(username):
                failed_count += 1
                failed_idx.append(i+1)
                failed_reason.append(Consts.USER_EXISTED_MSG)
                continue
            try:
                # todo: generate random password and send email to user
                password = "88888888"
                create_user(username, password, name, phone, email)
                success_count += 1
            except:
                failed_count += 1
                failed_idx.append(i+1)
                failed_reason.append(Consts.UNKNOWN_ERROR)
        result.code = Consts.SUCCESS_CODE
        if failed_count > 0:
            result.msg = u"成功导入%d条数据, 失败%d条, 原因: \n" % (success_count, failed_count)
            for i, r in zip(failed_idx, failed_reason):
                result.msg += "第%d行, %s \n" % (i, r)
        else:
            result.msg = u"成功导入%d条数据" % success_count
    except Exception as e:
        result.code = Consts.FAILED_CODE
        result.msg = e.message
        raise e
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def remove_admin(request, username):
    result = Result()
    try:
        remove_user(username)
        result.code = Consts.SUCCESS_CODE
    except User.DoesNotExist:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.NOT_FOUND_USER_MSG
    except:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


def login(request):
    return render(request, 'login.html')


def no_permission(request):
    return render(request, 'no_permission.html')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url="/backend/no_permission")
def create_admin(request):
    result = Result()
    username = request.POST['username']
    name = request.POST['name']
    # todo: generate random password and send email to user
    password = "88888888"
    email = request.POST['email']
    phone = request.POST['phone']
    if is_username_valid(username):
        result.code = Consts.FAILED_CODE
        result.msg = Consts.USER_EXISTED_MSG
    else:
        try:
            create_user(username, password, name, phone, email)
            result.code = Consts.SUCCESS_CODE
        except:
            result.code = Consts.FAILED_CODE
            result.msg = Consts.UNKNOWN_ERROR
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")


def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    result = Result()
    if user:
        _login(request=request, user=user)
        result.code = Consts.SUCCESS_CODE
    else:
        result.code = Consts.FAILED_CODE
        result.msg = Consts.LOGIN_FAILED_MSG
    return HttpResponse(json.dumps(result.to_dict()), content_type="application/json")

