import os
import re
import shutil
import calendar
import datetime
import xlrd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from webapp.shortcuts.decorator import permission_required
from webapp.const import Company
from webapp.models import *
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *
from webapp.utils.query import get_query, create_data


def index(request, template_name):
    """
    查询/展示 页面
    """
    page_dict = {}
    pCompany = COMPANY_CHOICE
    # maturity =
    # independence =
    # business =
    # technology =
    page_dict.update({"pCompany": pCompany})
    return render(request, template_name, page_dict)



def jump(request, template_name):
    return render(request, template_name)


@csrf_exempt
# 查询页签数据
def search(request):
    # fil = {"status": ProductStatus.PASS, "is_vaild": True}
    fil = {"is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)