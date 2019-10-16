import os
import re
import shutil
import calendar
import datetime
import xlrd
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1)
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2)
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3)
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4)

    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
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


@csrf_exempt
# 展示页面数据
def show(request, template_name):
    """
    查询/展示 页面
    """
    page_dict = {}
    pCompany = COMPANY_CHOICE
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1)
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2)
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3)
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4)
    maturity_product = {}
    independence_product = {}
    business_product = {}
    technology_product = {}
    for i in maturity:
        product_list = Product.objects.filter(maturity__first_class=i.first_class)
        num = len(product_list)
        # print(num)
        maturity_product.update({i.meaning: num})
    for i in independence:
        product_list = Product.objects.filter(independence__first_class=i.first_class)
        num = len(product_list)
        # print(num)
        independence_product.update({i.meaning: num})
    for i in business:
        product_list = Product.objects.filter(business__first_class=i.first_class)
        num = len(product_list)
        # print(num)
        business_product.update({i.meaning: num})
    for i in technology:
        product_list = Product.objects.filter(technology__first_class=i.first_class)
        num = len(product_list)
        # print(num)
        technology_product.update({i.meaning: num})
    print(maturity_product)
    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology,
                      "maturity_product": maturity_product,
                      "independence_product": independence_product,
                      "business_product": business_product,
                      "technology_product": technology_product})
    return render(request, template_name, page_dict)
