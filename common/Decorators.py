# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Consts
import urllib
from django.shortcuts import redirect, reverse


def wechat_auth_required(function):
    def wrap(request, *args, **kwargs):
        if 'code' not in request.GET:
            view_name = function.__name__
            redirect_uri = request.build_absolute_uri(reverse(view_name, args=args))
            if request.is_secure() and not redirect_uri.startswith('https://'):
                redirect_uri = redirect_uri.replace("http", "https")
            print "is_secure: %s, redirect_uri: %s" % (request.is_secure(), redirect_uri)

            return redirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s" \
                            % (Consts.APPID, urllib.quote(redirect_uri, safe=""), "snsapi_base", "123#wechat_sign"))
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
