# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-05-25 13:51

from django import template
from urllib import parse

register = template.Library()


@register.filter()
def contains(url, val):
    if url is None or val is None:
        return False

    return val in url


@register.filter()
def widget_with_classes(value, arg):
    return value.as_widget(attrs={'class': arg})
