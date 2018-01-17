# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login as _login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
import consts


@login_required
def index(request):
    data = {
        "pageName": "首页"
    }
    return render(request, 'index.html', data)


def login(request):
    return render(request, 'login.html')


def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    message = {}
    if user:
        _login(request=request, user=user)
        message['status'] = consts.SUCCESS_CODE
    else:
        message['status'] = consts.FAILED_CODE
        message['info'] = consts.LOGIN_FAILED_MSG
    return HttpResponse(json.dumps(message), content_type="application/json")