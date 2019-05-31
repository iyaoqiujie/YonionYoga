# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-05-29 10:41

from django import forms


class CertQueryForm(forms.Form):
    """
    A form for querying a yoga cert exists or not
    """
    user_name = forms.CharField(label='证书持有者姓名')
    cert_id = forms.CharField(label='证书编号')
